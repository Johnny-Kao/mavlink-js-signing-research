#!/usr/bin/env python3
"""Patch only upstream JavaScript_NextGen generator replay-state bookkeeping."""

from pathlib import Path
import sys


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: apply_fix.py <upstream-pymavlink-directory>")
    path = Path(sys.argv[1]) / "generator/mavgen_javascript.py"
    original = path.read_text(encoding="utf-8")
    early = """        this.signing.stream_timestamps[stream_key] = timestamp;
        //console.log('new stream',this.signing.stream_timestamps)
"""
    after_validation = """    if (!signaturesMatch) {
        return false;
    }
"""
    if original.count(early) != 1 or original.count(after_validation) != 1:
        raise SystemExit("upstream changed: expected signing control-flow anchors missing")
    updated = original.replace(early, "", 1).replace(
        after_validation,
        after_validation + """    // Only authenticated packets advance per-stream replay state.
    this.signing.stream_timestamps[stream_key] = timestamp;
""",
        1,
    )
    path.write_text(updated, encoding="utf-8")
    print("Applied minimal JavaScript_NextGen signing-state fix.")


if __name__ == "__main__":
    main()
