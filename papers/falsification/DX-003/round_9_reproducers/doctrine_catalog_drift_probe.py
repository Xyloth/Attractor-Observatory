import ast, json, re
from pathlib import Path
init=Path('CLAUDE_BUILDER_INITIATION.md').read_text(encoding='utf-8', errors='replace')
readme=Path('README.md').read_text(encoding='utf-8', errors='replace')
ai_ops=Path('control_room/rooms/ai_operations_tower.py').read_text(encoding='utf-8', errors='replace')
doctrine_console=Path('control_room/rooms/doctrine_console.py').read_text(encoding='utf-8', errors='replace')
registry=json.loads(Path('docs/doctrine_registry.json').read_text(encoding='utf-8'))
classes_init=sorted({int(x) for x in re.findall(r'^### Class (\d+)\b', init, flags=re.M)})
classes_readme=sorted({int(x) for x in re.findall(r'Class (\d+)\b', readme)})
def extract_catalog_count(py_text):
    mod=ast.parse(py_text)
    for node in mod.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id=='MISTAKE_CATALOG':
                    value=ast.literal_eval(node.value)
                    return len(value), [str(row[0]) for row in value]
    return None, []
ai_count, ai_ids=extract_catalog_count(ai_ops)
doc_count, doc_ids=extract_catalog_count(doctrine_console)
registry_ids=[row['id'] for row in registry['doctrines']]
out={
 'claude_builder_initiation_class_ids': classes_init,
 'claude_builder_initiation_class_count': len(classes_init),
 'readme_mentions_class_13': 'Class 13' in readme,
 'ai_operations_catalog_count': ai_count,
 'ai_operations_catalog_ids': ai_ids,
 'ai_operations_class_13_present': '13' in ai_ids or 'Class 13' in ai_ops,
 'doctrine_console_catalog_count': doc_count,
 'doctrine_console_catalog_ids': doc_ids,
 'doctrine_console_class_13_present': '13' in doc_ids or 'Class 13' in doctrine_console,
 'doctrine_registry_ids_tail': registry_ids[-8:],
 'doctrine_registry_count': len(registry_ids),
 'doctrine_console_mentions_d7_d22': 'D7 — D22' in doctrine_console or 'D7-D22' in doctrine_console or 'D7 â€” D22' in doctrine_console,
 'control_room_rooms_readme_mentions': [line for line in Path('control_room/rooms/README.md').read_text(encoding='utf-8', errors='replace').splitlines() if 'Class 1-12' in line or 'D7-D25' in line],
 'portfolio_demo_mentions': [line for line in Path('control_room/rooms/portfolio_demo.py').read_text(encoding='utf-8', errors='replace').splitlines() if 'D7-D22' in line or 'Class 1-12' in line],
}
Path('papers/falsification/DX-003/round_9_reproducers/doctrine_catalog_drift_probe.json').write_text(json.dumps(out, indent=2, sort_keys=True), encoding='utf-8')
lines=[]
for key in ['claude_builder_initiation_class_count','claude_builder_initiation_class_ids','readme_mentions_class_13','ai_operations_catalog_count','ai_operations_catalog_ids','ai_operations_class_13_present','doctrine_console_catalog_count','doctrine_console_catalog_ids','doctrine_console_class_13_present','doctrine_registry_count','doctrine_registry_ids_tail','doctrine_console_mentions_d7_d22']:
    lines.append(f'{key}={out[key]}')
for line in out['control_room_rooms_readme_mentions']:
    lines.append('control_room_rooms_README=' + line)
for line in out['portfolio_demo_mentions']:
    lines.append('portfolio_demo=' + line)
Path('papers/falsification/DX-003/round_9_reproducers/doctrine_catalog_drift_probe.txt').write_text('\n'.join(lines)+'\n', encoding='utf-8')
print('\n'.join(lines).encode('ascii','backslashreplace').decode('ascii'))
