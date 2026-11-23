#!/usr/bin/env python3
"""Audita la version seleccionada de AndroidX Fragment en releaseRuntimeClasspath.

dependencyInsight puede mostrar '1.0.0 -> 1.9.1': eso indica que la
version solicitada fue sustituida, no que se distribuya la version antigua.
"""
from pathlib import Path
import re
import sys

if len(sys.argv) != 2:
    sys.exit("Uso: check_fragment_release.py <reporte dependencyInsight>")
report = Path(sys.argv[1]).read_text(encoding="utf-8")
report = re.sub(r"\x1b\[[0-9;]*m", "", report)
if "No dependencies matching given input were found" in report:
    print("PASS: Fragment no forma parte de releaseRuntimeClasspath.")
    sys.exit(0)
selected = re.search(r"(?m)^androidx\.fragment:fragment:([0-9][^\s(]*)", report)
if selected is None:
    sys.exit("ERROR: no se pudo comprobar la version resuelta de AndroidX Fragment.")
version = selected.group(1)
if version == "1.0.0":
    sys.exit("ERROR: AndroidX Fragment 1.0.0 sigue seleccionado en release.")
if not version.startswith("1.9.1"):
    sys.exit(f"REVISAR: version de Fragment distinta de la esperada: {version}")
print(f"PASS: Fragment seleccionado para releaseRuntimeClasspath: {version}")
