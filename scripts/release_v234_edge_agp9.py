#!/usr/bin/env python3
"""v2.3.4 code25: replace edge-to-edge helper that invokes deprecated APIs.
Runs after release_v233_ads.py; preserve ad layouts, SDK floors, 50 assets, and R8.
"""
from pathlib import Path

src=Path("app/src/main/java/gratis/lazosdeluto/MainActivity.java")
s=src.read_text(encoding="utf-8")
old=""" @Override protected void onPostCreate(android.os.Bundle savedInstanceState) {
  super.onPostCreate(savedInstanceState);
  androidx.core.view.WindowCompat.enableEdgeToEdge(getWindow());
 }"""
new=""" @Override protected void onPostCreate(android.os.Bundle savedInstanceState) {
  super.onPostCreate(savedInstanceState);
  // Layout edge-to-edge without WindowCompat.enableEdgeToEdge, which can call
  // deprecated bar-color setters and SHORT_EDGES on supported Android versions.
  androidx.core.view.WindowCompat.setDecorFitsSystemWindows(getWindow(), false);
  // Do not call setStatusBarColor or setNavigationBarColor.
  // Status/navigation icons remain legible against the app's light background.
  androidx.core.view.WindowInsetsControllerCompat controller =
      androidx.core.view.WindowCompat.getInsetsController(getWindow(), getWindow().getDecorView());
  controller.setAppearanceLightStatusBars(true);
  controller.setAppearanceLightNavigationBars(true);
  if(android.os.Build.VERSION.SDK_INT>=28){
   android.view.WindowManager.LayoutParams attributes=getWindow().getAttributes();
   attributes.layoutInDisplayCutoutMode=
       android.view.WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_ALWAYS;
   getWindow().setAttributes(attributes);
  }
  if(android.os.Build.VERSION.SDK_INT>=29){
   getWindow().setNavigationBarContrastEnforced(false);
  }
 }"""
assert s.count(old)==1, "Unexpected edge-to-edge implementation"
s=s.replace(old,new,1)
for disallowed in ("WindowCompat.enableEdgeToEdge(", "setStatusBarColor(",
                   "setNavigationBarColor(", "LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES"):
    # Only check actual code, strip code comments that name APIs for audit.
    code="\n".join(line for line in s.splitlines() if not line.lstrip().startswith("//"))
    assert disallowed not in code, disallowed
src.write_text(s,encoding="utf-8")

# The legacy source ZIP is unpacked at the beginning of CI and can replace
# the top-level build.gradle. Enforce AGP 9 after the unpacking step.
root_gradle=Path("build.gradle")
root_content=root_gradle.read_text(encoding="utf-8")
if "version '8.11.1'" in root_content:
    root_content=root_content.replace("version '8.11.1'","version '9.0.1'",1)
assert "version '9.0.1'" in root_content, "AGP 9.0.1 missing after ZIP unpack"
root_gradle.write_text(root_content,encoding="utf-8")

gradle=Path("app/build.gradle")
g=gradle.read_text(encoding="utf-8")
assert g.count("versionCode 24")==1 and g.count("versionName '2.3.3'")==1
assert "minifyEnabled true" in g and "shrinkResources true" in g
g=g.replace("versionCode 24","versionCode 25",1).replace(
  "versionName '2.3.3'","versionName '2.3.4'",1)
gradle.write_text(g,encoding="utf-8")
print("v2.3.4 code25: Android 15 edge-to-edge without deprecated bar setter/cutout APIs")
