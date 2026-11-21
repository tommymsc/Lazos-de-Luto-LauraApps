#!/usr/bin/env python3
"""Lazos 2.2.7: cold-start App Open lifecycle and diagnostic logging.

Applied AFTER upgrade_ui, monetization_v22, compatibility_api23 and
compatibility_api19. No ad-ID, privacy, target/min-SDK or feature changes.
"""
from pathlib import Path

source=Path("app/src/main/java/gratis/lazosdeluto/MainActivity.java")
s=source.read_text(encoding="utf-8")
def replace_once(old,new,label):
 global s
 n=s.count(old)
 if n!=1: raise RuntimeError(f"{label}: expected once, found {n}")
 s=s.replace(old,new,1)

# The previous version skipped App Open for the first two launches entirely.
replace_once('if(launches>=2 && !BuildConfig.APP_OPEN_ID.isEmpty()){',
             'if(!BuildConfig.APP_OPEN_ID.isEmpty()){',
             'open ad on each cold launch')

# Give asynchronous consent + ads a reasonable bounded window, not 1.7 seconds.
replace_once('mainHandler.postDelayed(()->finishOpeningScreen(),1700L);',
             'mainHandler.postDelayed(()->{if(!fullScreenActive)finishOpeningScreen();},6500L);',
             'bounded launch gate')

# A late loaded ad is never allowed to overlay an already interactive screen.
replace_once('  openingScreen=false;\n  showHome();',
             '  openingScreen=false;\n  openingAd=null;\n  showHome();',
             'close and discard stale opening ad')

# A loaded App Open ad can be shown once only on startup; log unsuccessful fills.
replace_once('   @Override public void onAdFailedToLoad(LoadAdError err){openingLoading=false;finishOpeningScreen();}',
             '   @Override public void onAdFailedToLoad(LoadAdError err){openingLoading=false;android.util.Log.w("LazosAds","App Open not filled: "+err.getCode());finishOpeningScreen();}',
             'open load diagnostics')

# Banner and interstitial requests may be unsuccessful even while the banner works.
replace_once('    @Override public void onAdFailedToLoad(LoadAdError error){interstitial=null;}',
             '    @Override public void onAdFailedToLoad(LoadAdError error){interstitial=null;android.util.Log.w("LazosAds","Interstitial not filled: "+error.getCode());}',
             'interstitial diagnostic')

# Never show a category interstitial if the activity has been backgrounded.
replace_once('if(transition && interstitial!=null && !fullScreenActive',
             'if(transition && interstitial!=null && !fullScreenActive && !isFinishing()',
             'category display guard')

source.write_text(s,encoding="utf-8")

gradle=Path("app/build.gradle")
g=gradle.read_text(encoding="utf-8")
assert g.count('versionCode 17')==1 and g.count("versionName '2.2.6'")==1
g=g.replace('versionCode 17','versionCode 18').replace("versionName '2.2.6'","versionName '2.2.7'")
gradle.write_text(g,encoding="utf-8")
assert 'versionCode 18' in g and 'minSdk 19' in g and 'targetSdk 36' in g
assert 'APP_OPEN_ID' in s and 'CATEGORY_AD_COOLDOWN_MS=120000L' in s
print("Lazos v2.2.7 code 18: cold-start App Open fix, bounded timeout, logging, existing cooldown preserved.")
