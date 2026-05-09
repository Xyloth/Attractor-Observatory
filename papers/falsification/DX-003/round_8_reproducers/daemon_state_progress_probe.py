import json
from pathlib import Path
state_path=Path('project_telemetry/factory_daemon_state.json')
sessions_path=Path('project_telemetry/factory_daemon_sessions.jsonl')
progress_root=Path('reports/factory_daemon_progress')
state=json.loads(state_path.read_text(encoding='utf-8'))
sessions=[]
for line in sessions_path.read_text(encoding='utf-8').splitlines():
    if line.strip():
        sessions.append(json.loads(line))
last_session=sessions[-1] if sessions else None
progress=[]
for path in sorted(progress_root.glob('*.json')):
    item=json.loads(path.read_text(encoding='utf-8'))
    item['_path']=path.as_posix()
    progress.append(item)
state_success=set((state.get('last_success_by_source') or {}).keys())
progress_completed={src for item in progress for src in item.get('sources_completed', [])}
progress_pending={src for item in progress for src in item.get('sources_pending', [])}
progress_written=sorted({item.get('written_at') for item in progress})
progress_sessions=sorted({item.get('session_id') for item in progress})
last_clearance=None
for item in reversed(sessions):
    if item.get('record_type')=='force_refresh_clearance':
        last_clearance=item
        break
stale_after_clear=[]
if last_clearance:
    cleared_at=last_clearance.get('cleared_at')
    for item in progress:
        if item.get('written_at','') < cleared_at and item.get('sources_completed'):
            stale_after_clear.append({'path':item['_path'], 'written_at':item.get('written_at'), 'sources_completed':item.get('sources_completed'), 'sources_pending':item.get('sources_pending'), 'last_clean_cycle':item.get('last_clean_cycle')})
summary={
    'state_last_success_count': len(state_success),
    'state_last_success_sources': sorted(state_success),
    'session_record_count': len(sessions),
    'last_session': last_session,
    'last_force_refresh_clearance': last_clearance,
    'progress_file_count': len(progress),
    'progress_written_at_values': progress_written,
    'progress_session_ids': progress_sessions,
    'progress_completed_sources': sorted(progress_completed),
    'progress_pending_sources': sorted(progress_pending),
    'progress_files_with_completed_sources_after_force_clear_count': len(stale_after_clear),
    'progress_files_with_completed_sources_after_force_clear_examples': stale_after_clear[:10],
    'progress_audit_queue_values': sorted({item.get('audit_queue_at_last_check') for item in progress}),
}
Path('papers/falsification/DX-003/round_8_reproducers/daemon_state_progress_probe.json').write_text(json.dumps(summary, indent=2, sort_keys=True), encoding='utf-8')
lines=[]
for key in ['state_last_success_count','session_record_count','progress_file_count','progress_written_at_values','progress_session_ids','progress_completed_sources','progress_pending_sources','progress_files_with_completed_sources_after_force_clear_count','progress_audit_queue_values']:
    lines.append(f'{key}={summary[key]}')
lines.append('last_force_refresh_clearance=' + json.dumps(last_clearance, sort_keys=True))
for item in summary['progress_files_with_completed_sources_after_force_clear_examples'][:5]:
    lines.append('stale_progress_example=' + json.dumps(item, sort_keys=True))
Path('papers/falsification/DX-003/round_8_reproducers/daemon_state_progress_probe.txt').write_text('\n'.join(lines)+'\n', encoding='utf-8')
print('\n'.join(lines))
