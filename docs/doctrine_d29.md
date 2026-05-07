# Doctrine D29 - Runnable Evidence

Mode: foundational  
Signed-by: Codex 1.5x (TASK-DX-002-FIX), under PI/Architect ratification

D29 - Reports naming enforcement modules, executable lenses, runtime paths, or
implementation files must either ship the named code in the public branch, mark
each citation as `evidence_private: true` / `private_unshipped` at point of use,
or downgrade the citation to narrative evidence. Reports cannot honestly claim
runnable verification while citing modules absent from the public branch without
explicit private-evidence markers.

## Failure mode caught

DX-002 found Campaign 023/024 and methods documents naming private runtime
modules such as `formalism/*`, `trace/*`, `worlds/*`, and validation code while
the public branch intentionally omitted those trees. The methodology may be
valid, but the public surface was ambiguous about whether the executable support
was shipped.

## How enforced

Public JSON reports carry explicit private-runtime markers when a result depends
on private code. Public docs carry a runtime-boundary notice when they refer to
private implementation paths. Public tests exercise shipped public invariants
or gracefully stay within narrative/report surfaces; they do not imply private
runtime reproducibility.
