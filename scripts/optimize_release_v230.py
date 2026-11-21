#!/usr/bin/env python3
"""Configure R8 release optimization and constrain transitive AndroidX Fragment.
Runs only AFTER v2.2.9 SDK script. Does not touch ad IDs, SDK floors, or app behavior.
"""
from pathlib import Path
p=Path("app/build.gradle")
s=p.read_text(encoding="utf-8")
assert s.count("release { minifyEnabled false;")==1
assert s.count("versionCode 20")==1
assert s.count("versionName '2.2.9'")==1
assert "minSdk 23" in s and "targetSdk 36" in s
s=s.replace("release { minifyEnabled false;",
 """release { minifyEnabled true; shrinkResources true;
   proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro';""",1)
s=s.replace("versionCode 20","versionCode 21",1).replace("versionName '2.2.9'","versionName '2.3.0'",1)
# Constraints only select the version if some dependency actually pulls in Fragment.
# No new Fragment library is added to the app unnecessarily.
anchor="dependencies {"
assert s.count(anchor)==1
s=s.replace(anchor,"""dependencies {
 constraints {
  implementation('androidx.fragment:fragment:1.9.1') {
   because 'Keep any transitive AndroidX Fragment on a maintained stable release'
  }
 }
""",1)
p.write_text(s,encoding="utf-8")
assert "minifyEnabled true" in s and "shrinkResources true" in s
assert "proguard-android-optimize.txt" in s and "versionCode 21" in s
print("Lazos v2.3.0 code21: release R8, resource shrinker, and conditional Fragment 1.9.1 constraint configured.")
