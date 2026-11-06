# Verified findings — 2026-11-06

## Tested source

- Upstream: `ArduPilot/pymavlink@544d9016f6e19fed105b28fb41e9ade19c45d8c2`
- Generator: `generator/mavgen_javascript.py` (`JavaScript_NextGen`)
- Test fixture: upstream `tests/snapshottests/resources/minimal.xml`
- Public [GitHub Actions verification](https://github.com/Johnny-Kao/mavlink-js-signing-research/actions/runs/42223328340)

## Confirmed failure

The generated `MAVLink20Processor.prototype.check_signature` writes the first observed stream timestamp *before* comparing the received signature with the expected digest. On an established stream, it does not update the per-stream timestamp after a valid, newer message.

These violate two established signing invariants and can lead to:

1. a malformed signed packet locking out a later legitimate packet on a previously unseen stream;
2. an already accepted signed packet being accepted a second time on an established stream, after a newer legitimate timestamp.

## Reproduction results

| Test job | Research JS tests | Upstream tests | Job |
| --- | --- | --- | --- |
| Original, Node 20 | 0 passed, 6 failed (expected) | Not run | PASS |
| Original, Node 22 | 0 passed, 6 failed (expected) | Not run | PASS |
| Candidate, Node 20 | 6 passed, 0 failed | Python signing: 12 passed; JS parser: 3 passed | PASS |
| Candidate, Node 22 | 6 passed, 0 failed | Python signing: 12 passed; JS parser: 3 passed | PASS |

Both baseline and candidate are generated from the same pinned upstream source. Research tests create real MAVLink 2 heartbeat packets through generated `heartbeat.pack()`, verify their cryptographic tags and invoke generated signing APIs. Two tests also use generated `decode()`, including the permissive `allow_unsigned_callback` policy.

The baseline matrix **intentionally requires failure** of the newly added regression tests. A baseline PASS therefore means *the expected failure was reproduced*, not that the original generator was correct.

## Minimal candidate change

`scripts/apply_fix.py` moves the existing per-stream timestamp assignment from the new-stream branch to the common post-signature-verification success path. It adds no public API, changes no message definitions, leaves SHA-256 signing unchanged, and preserves the pre-existing freshness / timestamp monotonicity checks.

## Prior art and maintainer context

Python's equivalent bug was fixed by [pymavlink #1301](https://github.com/ArduPilot/pymavlink/pull/1301), and its review explicitly recommended a JavaScript follow-up. The separate `JavaScript_Stable` generator already updates the per-stream timestamp after validation.

No upstream PR or issue has been created from this research.

## Boundaries

Verified on GitHub-hosted Ubuntu / Node.js 20 and 22 with current upstream generator and fixture. Other platforms, browser mode and broader interoperability matrices have not been executed. This is a focused correctness/security regression result, **not** a claim of a deployed exploit or an exhaustive review of every MAVLink generator.
