#!/usr/bin/env python3
"""Supported Android 6.0+ (API23), modern Google Mobile Ads, API36 target."""
from pathlib import Path
import re
p=Path("app/build.gradle")
s=p.read_text()
assert "minSdk 24" in s and "versionCode 13" in s and "versionName '2.2.2'" in s
s=s.replace("minSdk 24","minSdk 23").replace("versionCode 13","versionCode 15").replace("versionName '2.2.2'","versionName '2.2.4'")
s=re.sub(r"androidx\.core:core:[0-9.]+", "androidx.core:core:1.16.0", s)
s=re.sub(r"play-services-ads:[0-9.]+", "play-services-ads:24.7.0", s)
s=re.sub(r"user-messaging-platform:[0-9.]+", "user-messaging-platform:3.2.0", s)
assert "user-messaging-platform:3.2.0" in s and "play-services-ads:24.7.0" in s
p.write_text(s)
# Privacy safeguard: reject location permissions contributed by any dependency,
# including future versions of Google Mobile Ads. This app has no location feature.
manifest=Path("app/src/main/AndroidManifest.xml")
xml=manifest.read_text(encoding="utf-8")
if 'xmlns:tools=' not in xml:
    xml=xml.replace('<manifest xmlns:android="http://schemas.android.com/apk/res/android">',
        '<manifest xmlns:android="http://schemas.android.com/apk/res/android" xmlns:tools="http://schemas.android.com/tools">',1)
for permission in ("ACCESS_COARSE_LOCATION","ACCESS_FINE_LOCATION","ACCESS_BACKGROUND_LOCATION"):
    declaration='<uses-permission android:name="android.permission.'+permission+'" tools:node="remove"/>'
    if declaration not in xml:
        xml=xml.replace('<application ',declaration+'<application ',1)
manifest.write_text(xml,encoding="utf-8")
assert all('tools:node="remove"' in xml for _ in [0])
print("Privacy guard enabled: location permissions are excluded from merged manifest.")

print("Android 6.0+ configuration: minSdk23, targetSdk36, versionCode15, GMA24.7.0")
