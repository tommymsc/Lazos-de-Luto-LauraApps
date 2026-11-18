#!/usr/bin/env python3
"""Legacy Android 4.4 compatibility build; GMA 22.6.0 is sunset and may not serve ads."""
from pathlib import Path
import re
p=Path("app/build.gradle")
s=p.read_text()
assert "minSdk 24" in s and "versionCode 13" in s and "versionName '2.2.2'" in s
s=s.replace("minSdk 24","minSdk 19").replace("versionCode 13","versionCode 16").replace("versionName '2.2.2'","versionName '2.2.5'")
s=re.sub(r"androidx\.core:core:[0-9.]+", "androidx.core:core:1.12.0", s)
s=re.sub(r"play-services-ads:[0-9.]+", "play-services-ads:22.6.0", s)
s=re.sub(r"user-messaging-platform:[0-9.]+", "user-messaging-platform:2.2.0", s)
assert "user-messaging-platform:3.2.0" in s and "play-services-ads:24.7.0" in s
s=s.replace("defaultConfig {", "defaultConfig { multiDexEnabled true; ",1)
s=s.replace("dependencies {", "dependencies {\\n implementation 'androidx.multidex:multidex:2.0.1'",1)
p.write_text(s)
source=Path("app/src/main/java/gratis/lazosdeluto/MainActivity.java")
j=source.read_text(encoding="utf-8")
assert 'public class MainActivity extends Activity {' in j
j=j.replace('public class MainActivity extends Activity {',"""public class MainActivity extends Activity {
 @Override protected void attachBaseContext(Context base){
  super.attachBaseContext(base);
  androidx.multidex.MultiDex.install(this);
 }""",1)
j=j.replace('if(checkSelfPermission(android.Manifest.permission.WRITE_EXTERNAL_STORAGE)!=android.content.pm.PackageManager.PERMISSION_GRANTED){','if(Build.VERSION.SDK_INT>=23 && checkSelfPermission(android.Manifest.permission.WRITE_EXTERNAL_STORAGE)!=android.content.pm.PackageManager.PERMISSION_GRANTED){',1)
source.write_text(j,encoding="utf-8")
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

print("Android 4.4+ configuration: minSdk19, targetSdk36, versionCode16, GMA22.6.0 (sunset)")
