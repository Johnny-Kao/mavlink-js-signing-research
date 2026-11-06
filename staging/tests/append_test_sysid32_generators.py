

def test_nextgen_signing_replay_state(tmp_path):
    """Signed frames cannot poison authenticated state or bypass replay checks."""
    xml = Path(__file__).parent / 'snapshottests/resources/minimal.xml'
    generated = generate(tmp_path / 'mavlink.js', 'JavaScript_NextGen', xml=xml)
    env = node_environment()
    env['GENERATED_JS'] = str(generated)
    run([tool('node'), '--test', RESOURCES / 'signing-state.test.cjs'], env=env)
