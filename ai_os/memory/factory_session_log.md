# Factory Session Log

Status: template
Owner: Factory Claude
Created by: Codex Builder during Campaign 012

## Schema

Each Factory Claude session appends one entry after activation:

```text
timestamp_start:
timestamp_end:
factory_session_id:
model_name:
model_version:
adapter_id:
source_identity:
license_class:
mode:
ontology_registry_hash:
claims_extracted_count:
claims_normalized_count:
conflicts_flagged_count:
recommendations_produced_count:
audit_queue_depth_at_close:
license_closure_summary:
deferred_actions:
linked_artifacts:
```

## Entries

Factory Claude appends the first entry. Codex does not operate Factory sessions.
