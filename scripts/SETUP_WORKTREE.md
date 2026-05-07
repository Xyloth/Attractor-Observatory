# Worktree setup — required before running the daemon or Control Room

The Attractor Observatory keeps three runtime modules **outside git
tracking** for historical reasons (private contracts, derivative-work
hygiene, and per-Builder iteration speed):

* `formalism/` — lens registry, MotifContract, motif-side helpers
* `worlds/` — per-world simulation models
* `trace/` — trace schema + writer + verifier

Because they're listed in `.gitignore`, **`git worktree add` does
not bring them into a fresh worktree**. The daemon, the FIRE
button, and several `public_tests/test_task035_*` cases will crash
with `ModuleNotFoundError: No module named 'formalism'` until you
copy them in.

## Setup steps

```bash
# 1. Create the worktree as usual:
git worktree add "C:/Attractor Observatory DX Worktrees/my-task" -b feature/my-task main

# 2. Run the setup script from the new worktree:
cd "C:/Attractor Observatory DX Worktrees/my-task"
scripts/setup_worktree.sh             # POSIX (Git Bash / WSL / Linux)
# OR
scripts\setup_worktree.bat            # Windows native cmd / PowerShell

# 3. Verify:
python -c "import formalism, worlds, trace; print('ok')"
```

## What the script does

1. Resolves the main checkout (default `C:/Attractor Observatory`).
   Override by passing the path as the first argument.
2. Copies `formalism/`, `worlds/`, `trace/` from the main checkout
   into the new worktree.
3. Skips modules already present (idempotent — safe to re-run).
4. Reports progress + a verification one-liner.

## When to extend the script

If you add a new gitignored Python package that the daemon or the
Control Room imports, append it to the `modules` list in BOTH
`setup_worktree.sh` (line `modules=(formalism worlds trace)`) and
`setup_worktree.bat` (line `for %%D in (formalism worlds trace)`).

To find every gitignored module the daemon imports, run:

```bash
grep -E "^(from|import) (formalism|worlds|trace)" factory_lowlevel/*.py | sort -u
```

Then add any new package names to both scripts.

## Why these dirs are gitignored

Per `.gitignore` line 36:

```
formalism/
```

Historical: the formalism / worlds / trace layers carry private
contracts (motif predicates, world-model parameters that are
methodology-sensitive). Each Builder iterates locally; commits
landing in `papers/methods/` and `reports/campaign_*/` are the
public artifacts. The runtime modules stay private to each working
copy.

This pattern was working until cross-Builder worktree mechanics got
heavy (CB-008 onward). CB-011's audit identified the breakage; CB-013
ships the workaround. Long-term recommendation (escalated to
Architect): either remove these dirs from `.gitignore` so they ride
with the repo, or formalize a release tarball mechanism that ships
them alongside.

## Failure modes

* **Source path doesn't exist** — script exits with code 2 and a
  clear error.
* **xcopy/cp fails (permission, disk full)** — script exits with
  code 3.
* **Re-running** — script reports each present dir as "already
  present, skipping" rather than overwriting (D9: never silently
  overwrite a worktree's edits).
* **No git worktree at all** — script still runs; just copies into
  whatever the current directory's parent is.
