"""Check generated JavaScript_NextGen replay state using pymavlink test helpers.

Upstream placement: tests/test_javascript_signing_state.py
"""

from pathlib import Path

from test_sysid32_generators import generate, node_environment, run, tool

XML = Path(__file__).parent / "snapshottests/resources/minimal.xml"
NODE_TEST = Path(__file__).parent / "sysid32/signing-state.test.cjs"


def test_nextgen_signing_replay_state(tmp_path):
    generated = generate(tmp_path / "minimal.js", "JavaScript_NextGen", xml=XML)
    env = node_environment()
    env["GENERATED_JS"] = str(generated)
    run([tool("node"), "--test", NODE_TEST], env=env)
