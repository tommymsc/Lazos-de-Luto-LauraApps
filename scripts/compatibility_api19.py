#!/usr/bin/env python3
"""Android 4.4 compatibility build (API19), versionCode 14.
Legacy mobile ads is needed because supported 2026 Google Ads SDK requires API24.
WARNING: ads SDK 22.6.0 is sunset and ad fill is not guaranteed.
"""
from pathlib import Path
p=Path("app/build.gradle")
s=p.read_text()
assert "minSdk 24" in s and "versionCode 13" in s and "versionName '2.2.2'" in s
s=s.replace("minSdk 24","minSdk 19").replace("versionCode 13","versionCode 14").replace("versionName '2.2.2'","versionName '2.2.3'")
s=s.replace("androidx.core:core:1.16.0","androidx.core:core:1.12.0")
s=s.replace("play-services-ads:25.5.0","play-services-ads:22.6.0")
s=s.replace("user-messaging-platform:3.2.0","user-messaging-platform:2.2.0")
p.write_text(s)
p=Path("app/src/main/java/gratis/lazosdeluto/MainActivity.java")
s=p.read_text()
assert "if(Build.VERSION.SDK_INT<29){" in s
needle="""  if(Build.VERSION.SDK_INT<29){
   if(checkSelfPermission(android.Manifest.permission.WRITE_EXTERNAL_STORAGE)!=android.content.pm.PackageManager.PERMISSION_GRANTED){"""
repl="""  if(Build.VERSION.SDK_INT<29){
   if(Build.VERSION.SDK_INT>=23 && checkSelfPermission(android.Manifest.permission.WRITE_EXTERNAL_STORAGE)!=android.content.pm.PackageManager.PERMISSION_GRANTED){"""
assert needle in s
s=s.replace(needle,repl)
p.write_text(s)
print("Android 4.4+ configuration: minSdk19, targetSdk36, versionCode14")
