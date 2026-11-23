#!/usr/bin/env python3
"""CI regression tests for AndroidX Fragment dependency parser."""
import subprocess
import sys
import tempfile
from pathlib import Path

checker = Path("scripts/check_fragment_release.py")
cases = [
    ("androidx.fragment:fragment:1.0.0 -> 1.9.1\n", 0),
    ("androidx.fragment:fragment:1.9.1\n", 0),
    ("androidx.fragment:fragment:1.0.0\n", 1),
    ("No dependencies matching given input were found\n", 0),
    ("unknown Gradle report\n", 1),
]
for report, expected in cases:
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".txt") as f:
        f.write(report)
        f.flush()
        result = subprocess.run([sys.executable, str(checker), f.name], capture_output=True, text=True)
        assert (result.returncode == 0) == (expected == 0), (report, result.stdout, result.stderr)
print("Dependency report parser regression checks passed")
