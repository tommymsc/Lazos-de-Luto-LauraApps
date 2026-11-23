#!/usr/bin/env python3
"""Lazos 2.3.1 / versionCode 22. Upgrade without losing Android 6+ or existing AdMob."""
from pathlib import Path
p = Path("app/build.gradle")
s = p.read_text(encoding="utf-8")
for required in ("versionCode 21", "versionName '2.3.0'", "minSdk 23", "targetSdk 36", "minifyEnabled true", "shrinkResources true", "play-services-ads:24.7.0", "user-messaging-platform:3.2.0"):
    if required not in s:
        raise SystemExit(f"Release 2.3.0 prerequisite missing: {required}")
if s.count("versionCode 21") != 1 or s.count("versionName '2.3.0'") != 1:
    raise SystemExit("Ambiguous 2.3.0 version, refusing bump")
s = s.replace("versionCode 21", "versionCode 22", 1).replace("versionName '2.3.0'", "versionName '2.3.1'", 1)
# The constraint is already inserted by optimize_release_v230.py.
# Preserve its conditional nature (no Fragment dependency is added unnecessarily).
old = "implementation('androidx.fragment:fragment:1.9.1') {"
new = """implementation('androidx.fragment:fragment') {
   version { strictly '1.9.1' }"""
# Strict constraint may reject a dependency that requires another version:
# in that case CI must fail rather than ship the outdated library.
if s.count(old) != 1:
    raise SystemExit("Expected Fragment constraint missing")
# Keep the existing because clause and closing brackets.
s = s.replace(old, new, 1)
p.write_text(s, encoding="utf-8")
print("Lazos 2.3.1 code 22: Fragment strict 1.9.1, R8, GMA 24.7, UMP 3.2, minSdk23 and targetSdk36.")
