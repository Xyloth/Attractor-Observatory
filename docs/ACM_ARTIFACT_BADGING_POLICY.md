# Artifact Review and Badging Policy

Status: policy; no badge claimed.

The project does not currently claim ACM artifact badges. If submitted for review, the public branch would be presented as a narrative/audit surface with public smoke tests, while private runtime code and trace dumps would require controlled reviewer access from the PI.

## Current self-assessment

- Artifacts Available: partially. Public reports/docs are available; private runtime/trace artifacts are not public.
- Artifacts Evaluated - Functional: not claimed. Public tests validate public-surface invariants only.
- Results Reproduced/Replicated: not claimed from the public branch alone.

## Review package requirements before any claim

1. Commit all audit-live plans and doctrine at the review target SHA.
2. Provide reviewer access to private runtime code or downgrade all executable claims to narrative evidence.
3. Provide trace bundles or maintain `evidence_private` markers without claiming public rerunnability.
4. Include RO-Crate metadata, PROV-O graphs, FAIR metadata, and exact environment setup.
