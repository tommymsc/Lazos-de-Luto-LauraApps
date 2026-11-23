#!/usr/bin/env python3
"""Audita AndroidX Fragment en releaseRuntimeClasspath sin confundir version solicitada con resuelta."""
from pathlib import Path
import re
import sys

if len(sys.argv) != 2:
    sys.exit("Uso: check_fragment_release.py <reporte dependencyInsight>")

report_path = Path(sys.argv[1])
if not report_path.is_file():
    sys.exit(f"ERROR: falta reporte: {report_path}")
report = report_path.read_text(encoding="utf-8", errors="replace")
report = re.sub(r"\x1b\[[0-9;]*m", "", report)

if "No dependencies matching given input were found" in report:
    print("PASS: Fragment no aparece en releaseRuntimeClasspath.")
    sys.exit(0)

# Gradle dependencyInsight presenta encabezados de componente y puede incluir
# sustituciones del tipo '1.0.0 -> 1.9.1'. La seleccionada es la del destino.
versions = []
for line in report.splitlines():
    line = line.strip()
    match = re.match(r"^androidx\.fragment:fragment:([0-9][^\s()]*)", line)
    if not match:
        continue
    requested = match.group(1)
    redirected = re.search(r"\s+->\s+([0-9][^\s()]*)", line)
    selected = redirected.group(1) if redirected else requested
    versions.append(selected)

if not versions:
    print("INDETERMINADO: Gradle no mostró un encabezado de Fragment interpretable.")
    print("Inspeccionar el artefacto Lazos-Fragment-Dependency-Audit antes de publicar.")
    sys.exit(0)

if "1.0.0" in versions:
    sys.exit("ERROR: Fragment 1.0.0 parece seguir seleccionado en releaseRuntimeClasspath.")

if all(v.startswith("1.9.1") for v in versions):
    print("PASS: Fragment 1.9.1 seleccionado en releaseRuntimeClasspath.")
else:
    print(f"REVISAR: versiones seleccionadas de Fragment: {', '.join(sorted(set(versions)))}")
    print("No se confirma cumplimiento sin examinar el informe.")
