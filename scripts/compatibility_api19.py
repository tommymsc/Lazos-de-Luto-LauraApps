#!/usr/bin/env python3
"""Android 4.4 compatibility build (API19), versionCode 14.
Legacy mobile ads is needed because supported 2026 Google Ads SDK requires API24.
WARNING: ads SDK 22.6.0 is sunset and ad fill is not guaranteed.
"""
from pathlib import Path
import re
p=Path("app/build.gradle")
s=p.read_text()
assert "minSdk 24" in s and "versionCode 13" in s and "versionName '2.2.2'" in s
s=s.replace("minSdk 24","minSdk 19").replace("versionCode 13","versionCode 14").replace("versionName '2.2.2'","versionName '2.2.3'")
s=re.sub(r"androidx\.core:core:[0-9.]+", "androidx.core:core:1.12.0", s)
s=re.sub(r"play-services-ads:[0-9.]+", "play-services-ads:22.6.0", s)
s=re.sub(r"user-messaging-platform:[0-9.]+", "user-messaging-platform:2.2.0", s)
assert "user-messaging-platform:2.2.0" in s and "play-services-ads:22.6.0" in s
s=s.replace("defaultConfig {", "defaultConfig { multiDexEnabled true; ",1)
s=s.replace("dependencies {", "dependencies {\\n implementation 'androidx.multidex:multidex:2.0.1'",1)
p.write_text(s)
p=Path("app/src/main/java/gratis/lazosdeluto/MainActivity.java")
s=p.read_text()
assert "if(Build.VERSION.SDK_INT<29){" in s
assert "public class MainActivity extends Activity {" in s
s=s.replace("public class MainActivity extends Activity {", """public class MainActivity extends Activity {
 @Override protected void attachBaseContext(Context base){
  super.attachBaseContext(base);
  androidx.multidex.MultiDex.install(this);
 }""",1)
needle="""  if(Build.VERSION.SDK_INT<29){
   if(checkSelfPermission(android.Manifest.permission.WRITE_EXTERNAL_STORAGE)!=android.content.pm.PackageManager.PERMISSION_GRANTED){"""
repl="""  if(Build.VERSION.SDK_INT<29){
   if(Build.VERSION.SDK_INT>=23 && checkSelfPermission(android.Manifest.permission.WRITE_EXTERNAL_STORAGE)!=android.content.pm.PackageManager.PERMISSION_GRANTED){"""
assert needle in s
s=s.replace(needle,repl)
p.write_text(s)
print("Android 4.4+ configuration: minSdk19, targetSdk36, versionCode14")
