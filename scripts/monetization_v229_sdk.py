#!/usr/bin/env python3
"""Upgrade from sunset GMA 22.6.0 to supported 24.7.0.
SDK 24 requires minSdk 23. Preserve targetSdk and current placements.
"""
from pathlib import Path
p=Path("app/build.gradle")
s=p.read_text(encoding="utf-8")
assert s.count("minSdk 19")==1
assert s.count("versionCode 19")==1
assert s.count("versionName '2.2.8'")==1
assert s.count("play-services-ads:22.6.0")==1
assert s.count("user-messaging-platform:2.2.0")==1
s=s.replace("minSdk 19","minSdk 23")
s=s.replace("versionCode 19","versionCode 20")
s=s.replace("versionName '2.2.8'","versionName '2.2.9'")
s=s.replace("play-services-ads:22.6.0","play-services-ads:24.7.0")
s=s.replace("user-messaging-platform:2.2.0","user-messaging-platform:3.2.0")
assert "targetSdk 36" in s
p.write_text(s,encoding="utf-8")
print("v2.2.9 code20: GMA24.7.0 supported; UMP3.2.0; minSdk23, targetSdk36.")
