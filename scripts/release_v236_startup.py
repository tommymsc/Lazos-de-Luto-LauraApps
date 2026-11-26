#!/usr/bin/env python3
"""2.3.6 code 27: conservative startup hotfix, after all 2.3.5 ad changes."""
from pathlib import Path
p=Path("app/src/main/java/gratis/lazosdeluto/MainActivity.java")
s=p.read_text(encoding="utf-8")
def change(a,b):
 global s
 assert s.count(a)==1,(a,s.count(a))
 s=s.replace(a,b,1)
# Android 15+ enforces edge-to-edge for target 35+. Do not opt out or
# explicitly set obsolete cutout modes or system-bar contrast/color APIs.
start=s.index(" @Override protected void onPostCreate(android.os.Bundle savedInstanceState)")
end=s.index("\n }",start)+len("\n }")
old=s[start:end]
assert "LAYOUT_IN_DISPLAY_CUTOUT_MODE_ALWAYS" in old and "setNavigationBarContrastEnforced" in old
s=s[:start]+""" @Override protected void onPostCreate(android.os.Bundle savedInstanceState) {
  super.onPostCreate(savedInstanceState);
  if(android.os.Build.VERSION.SDK_INT<35){
   androidx.core.view.WindowCompat.setDecorFitsSystemWindows(getWindow(), false);
  }
  androidx.core.view.WindowInsetsControllerCompat controller =
      androidx.core.view.WindowCompat.getInsetsController(getWindow(), getWindow().getDecorView());
  controller.setAppearanceLightStatusBars(true);
  controller.setAppearanceLightNavigationBars(true);
 }"""+s[end:]
# Avoid old multidex bootstrapping: minSdk 23 uses native multidex.
change(""" @Override protected void attachBaseContext(Context base){
  super.attachBaseContext(base);
  androidx.multidex.MultiDex.install(this);
 }""","")
# Avoid preloading an App Open ad after the startup window has ended:
# these activities only display App Open ads on a cold-start cover.
change("if(!adsUsable() || BuildConfig.APP_OPEN_ID.isEmpty() || openingLoading || fullScreenActive)return;",
       "if(!openingScreen || !adsUsable() || BuildConfig.APP_OPEN_ID.isEmpty() || openingLoading || fullScreenActive)return;")
# Keep a request from attaching to an already destroyed or backgrounded screen.
change("if(!adsAllowed())return;\n    openingAd=loaded;","if(!adsAllowed() || !openingScreen || !adsForeground)return;\n    openingAd=loaded;")
p.write_text(s,encoding="utf-8")
gpath=Path("app/build.gradle")
g=gpath.read_text(encoding="utf-8")
for a in ("versionCode 26","versionName '2.3.5'","minifyEnabled true; shrinkResources true;","play-services-ads:24.7.0","user-messaging-platform:3.2.0","implementation 'androidx.multidex:multidex:2.0.1'"):
 assert g.count(a)==1,(a,g.count(a))
# Emergency stability build: temporarily turn off all R8 code rewriting
# and resource shrinking to isolate the startup failure seen in code 25.
g=g.replace("versionCode 26","versionCode 27",1).replace("versionName '2.3.5'","versionName '2.3.6'",1)
g=g.replace("minifyEnabled true; shrinkResources true;","minifyEnabled false; shrinkResources false;",1)
g=g.replace("play-services-ads:24.7.0","play-services-ads:25.4.0",1)
g=g.replace("user-messaging-platform:3.2.0","user-messaging-platform:4.0.0",1)
g=g.replace("implementation 'androidx.multidex:multidex:2.0.1'","implementation 'androidx.startup:startup-runtime:1.2.0'",1)
g=g.replace("multiDexEnabled true; ","",1)
assert "minSdk 23" in g and "targetSdk 36" in g
gpath.write_text(g,encoding="utf-8")
assert "LAYOUT_IN_DISPLAY_CUTOUT_MODE_ALWAYS" not in s
assert "setNavigationBarContrastEnforced(" not in s
assert "MultiDex.install(" not in s
print("2.3.6 code27: conservative unminified startup hotfix; API23 preserved; modern edge-to-edge; GMA25.4/UMP4")
