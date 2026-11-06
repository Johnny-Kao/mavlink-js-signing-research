# MAVLink JavaScript signing replay-state research

Public research harness for the `JavaScript_NextGen` generator from [ArduPilot/pymavlink](https://github.com/ArduPilot/pymavlink). This repo is not a fork or upstream PR.

## Scope

The internal signing/replay state must meet two invariants already enforced by upstream Python ([#1301](https://github.com/ArduPilot/pymavlink/pull/1301)):

- A rejected signature must not change authenticated stream timestamps.
- A valid signature must advance the source stream timestamp, so subsequent duplicates are rejected.

Upstream source is pinned to `544d9016f6e19fed105b28fb41e9ade19c45d8c2`. Research CI runs the original generator and a minimally modified copy at the **same** commit, generating a real MAVLink 2 JavaScript binding with upstream's `mavgen` and `tests/snapshottests/resources/minimal.xml` fixture.

## Validation

The public GitHub Actions matrix tests Node 20 and 22. The baseline is required to **fail** the new regression test, while the candidate must **pass**. Candidate jobs also invoke upstream `pytest` signing and targeted JavaScript parser tests. All tests run on public GitHub-hosted runners, not on the author's Mac.

The candidate only moves the stream timestamp assignment to after successful signature verification in `generator/mavgen_javascript.py`, without changing public APIs, signing algorithms, XML definitions or wire format. This candidate is provisional pending successful CI.

Historical context: [Python issue #1300](https://github.com/ArduPilot/pymavlink/issues/1300), [Python fix #1301](https://github.com/ArduPilot/pymavlink/pull/1301) (which explicitly mentions this JavaScript follow-up), and [cross-language implementation #1295](https://github.com/ArduPilot/pymavlink/pull/1295).

## Research outputs

- `scripts/apply_fix.py`: precisely scoped patch to an upstream worktree.
- `tests/signing-state.test.cjs`: generated sender + receiver regression cases.
- `.github/workflows/replay-state.yml`: reproducible original-versus-candidate comparison.

No upstream code or project history is copied into this repository. An eventual upstream PR, if appropriate, should add equivalent regression coverage within pymavlink's own test conventions.
