#!/usr/bin/env python3
from pathlib import Path
import re
p = Path("app/build/outputs/mapping/release/mapping.txt")
assert p.is_file() and p.stat().st_size, "Missing R8 mapping"
pairs = re.findall(r"^([^ ]+) -> ([^ ]+):$", p.read_text(encoding="utf-8"), re.M)
renamed = sum(a != b for a,b in pairs)
assert renamed, "No renamed classes in R8 mapping"
print(f"Renamed classes: {renamed}/{len(pairs)}")
