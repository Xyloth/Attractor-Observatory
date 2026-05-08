import json, re
from collections import Counter, defaultdict
from pathlib import Path
ledger = Path('project_telemetry/ai_builder_tasks.jsonl')
rows=[]
errors=[]
for lineno,line in enumerate(ledger.read_text(encoding='utf-8').splitlines(),1):
    if not line.strip():
        continue
    try:
        item=json.loads(line)
        item['_lineno']=lineno
        rows.append(item)
    except Exception as e:
        errors.append({'line':lineno,'error':str(e),'raw':line[:200]})
unique_tasks=sorted({r.get('task_id') for r in rows if r.get('task_id')})
by_model=Counter(r.get('model_name','<missing>') for r in rows)
by_task_records=defaultdict(list)
for r in rows:
    by_task_records[r.get('task_id','<missing>')].append(r)
record_type_counts=Counter(r.get('record_type','<missing>') for r in rows)
missing_required=[]
required=['task_id','record_type','model_name','task_class']
for r in rows:
    miss=[k for k in required if k not in r or r.get(k) in (None,'')]
    if miss:
        missing_required.append({'line':r['_lineno'],'task_id':r.get('task_id'), 'record_type':r.get('record_type'), 'missing':miss})
pass_null_actual=[]
for r in rows:
    if str(r.get('acceptance_outcome','')).startswith('pass') and r.get('actual_minutes') is None and r.get('record_type') in {'actual_update','actual','superseded_estimate'}:
        pass_null_actual.append({'line':r['_lineno'],'task_id':r.get('task_id'),'record_type':r.get('record_type'),'model_name':r.get('model_name'),'acceptance_outcome':r.get('acceptance_outcome')})
# README claims
readme=Path('README.md').read_text(encoding='utf-8', errors='replace')
claims=[]
for pattern in [r'ledger spans \*\*(\d+) tasks across (\w+) distinct AI builders\*\*', r'Codex Legacy\*\* \((\d+) tasks', r'Codex 1\.5x\*\* \((\d+) task', r'Claude Builder\*\* \((\d+) sequential UI tasks']:
    m=re.search(pattern, readme)
    claims.append({'pattern':pattern,'match':m.group(0) if m else None, 'groups':m.groups() if m else None})
# Model/task current counts.
model_task_counts=Counter()
for task_id, task_rows in by_task_records.items():
    # choose last row's model_name as task identity proxy
    model_task_counts[task_rows[-1].get('model_name','<missing>')] += 1
# rows after TASK-033 proving README outdated about 1 task
codex15_tasks=sorted({r.get('task_id') for r in rows if r.get('model_name')=='Codex 1.5x' and r.get('task_id')})
cb_tasks=sorted({r.get('task_id') for r in rows if r.get('model_name')=='Claude (Builder)' and r.get('task_id')})
# BUILD_LOG latest task mentions
build=Path('BUILD_LOG.md').read_text(encoding='utf-8', errors='replace')
mentioned=sorted(set(re.findall(r'TASK-[A-Z0-9_-]+', build)))
missing_from_build=[tid for tid in unique_tasks if tid and tid.startswith('TASK-') and tid not in mentioned]
# freshness of README claim: line extract
readme_lines=[]
for i,line in enumerate(readme.splitlines(),1):
    if 'ledger spans' in line or 'Codex 1.5x' in line or 'Claude Builder' in line and 'tasks' in line or '34 tasks across' in line:
        readme_lines.append({'line':i,'text':line})
out={
 'ledger_rows':len(rows),
 'json_errors':errors,
 'unique_task_count':len(unique_tasks),
 'record_type_counts':dict(record_type_counts),
 'row_model_counts':dict(by_model),
 'task_counts_by_last_model':dict(model_task_counts),
 'readme_claims':claims,
 'readme_relevant_lines':readme_lines,
 'codex_15x_unique_task_count':len(codex15_tasks),
 'codex_15x_tasks_first_20':codex15_tasks[:20],
 'claude_builder_unique_task_count':len(cb_tasks),
 'claude_builder_tasks_first_20':cb_tasks[:20],
 'missing_required_count':len(missing_required),
 'missing_required_examples':missing_required[:40],
 'pass_null_actual_count':len(pass_null_actual),
 'pass_null_actual_examples':pass_null_actual[:40],
 'task_ids_missing_from_BUILD_LOG_mention_count':len(missing_from_build),
 'task_ids_missing_from_BUILD_LOG_mention_examples':missing_from_build[:60],
}
Path('papers/falsification/DX-003/round_7_reproducers/telemetry_identity_probe.json').write_text(json.dumps(out, indent=2, sort_keys=True), encoding='utf-8')
lines=[]
lines.append(f"ledger_rows={out['ledger_rows']}")
lines.append(f"unique_task_count={out['unique_task_count']}")
lines.append(f"row_model_counts={out['row_model_counts']}")
lines.append(f"task_counts_by_last_model={out['task_counts_by_last_model']}")
lines.append(f"readme_claims={out['readme_claims']}")
lines.append(f"codex_15x_unique_task_count={out['codex_15x_unique_task_count']}")
lines.append(f"claude_builder_unique_task_count={out['claude_builder_unique_task_count']}")
lines.append(f"missing_required_count={out['missing_required_count']}")
lines.append(f"pass_null_actual_count={out['pass_null_actual_count']}")
lines.append(f"task_ids_missing_from_BUILD_LOG_mention_count={out['task_ids_missing_from_BUILD_LOG_mention_count']}")
for item in out['readme_relevant_lines'][:20]:
    lines.append(f"README:{item['line']}: {item['text']}")
Path('papers/falsification/DX-003/round_7_reproducers/telemetry_identity_probe.txt').write_text('\n'.join(lines)+'\n', encoding='utf-8')
print("\n".join(lines).encode("ascii", "backslashreplace").decode("ascii"))

