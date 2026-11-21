#!/usr/bin/env python3
"""Fix interstitial preload/retry/expiry for Lazos without extra ad placements.

Run after monetization_v227.py. Version 2.2.8 / code 19.
"""
from pathlib import Path
p=Path("app/src/main/java/gratis/lazosdeluto/MainActivity.java")
s=p.read_text(encoding="utf-8")
def change(a,b,title):
 global s
 n=s.count(a)
 if n!=1: raise RuntimeError(f"{title}: expected one occurrence, got {n}")
 s=s.replace(a,b,1)

change("private int previousCategory=0;",
"""private int previousCategory=0;
 private boolean interstitialLoading=false;
 private int interstitialLoadFailures=0;
 private long nextInterstitialRetryAt=0L;
 private long interstitialLoadedAt=0L;
 private static final long INTERSTITIAL_EXPIRY_MS=3600000L;""","interstitial state")
change("  if(transition && interstitial!=null && !fullScreenActive && !isFinishing()",
"""  // An interstitial is single-use and must not be stale; reload for a later transition.
  if(interstitial!=null && (now-interstitialLoadedAt)>=INTERSTITIAL_EXPIRY_MS){
   interstitial=null;
   interstitialLoadedAt=0L;
  }
  if(transition && interstitial!=null && !fullScreenActive && !isFinishing()""","category freshness")
change("  }else{navigate.run();}\n }\n private void showOpeningScreen(){",
"""  }else{
   navigate.run();
   if(interstitial==null)loadInterstitial();
  }
 }
 private void showOpeningScreen(){""","reload when no interstitial at natural boundary")
old=''' private void loadInterstitial(){
  if(BuildConfig.INTERSTITIAL_ID.isEmpty() || interstitial!=null || fullScreenActive)return;
  InterstitialAd.load(this,BuildConfig.INTERSTITIAL_ID,new AdRequest.Builder().build(),
   new InterstitialAdLoadCallback(){
    @Override public void onAdLoaded(InterstitialAd newAd){interstitial=newAd;}
    @Override public void onAdFailedToLoad(LoadAdError error){interstitial=null;android.util.Log.w("LazosAds","Interstitial not filled: "+error.getCode());}
   });
 }'''
new=''' private void loadInterstitial(){
  if(BuildConfig.INTERSTITIAL_ID.isEmpty() || isFinishing() || isDestroyed()
      || interstitialLoading || interstitial!=null || fullScreenActive
      || android.os.SystemClock.elapsedRealtime()<nextInterstitialRetryAt)return;
  interstitialLoading=true;
  InterstitialAd.load(this,BuildConfig.INTERSTITIAL_ID,new AdRequest.Builder().build(),
   new InterstitialAdLoadCallback(){
    @Override public void onAdLoaded(InterstitialAd loadedAd){
     interstitialLoading=false;
     interstitialLoadFailures=0;
     nextInterstitialRetryAt=0L;
     interstitialLoadedAt=android.os.SystemClock.elapsedRealtime();
     interstitial=loadedAd;
     android.util.Log.d("LazosAds","Interstitial cached for a future category transition");
    }
    @Override public void onAdFailedToLoad(LoadAdError error){
     interstitialLoading=false;
     interstitial=null;
     interstitialLoadedAt=0L;
     interstitialLoadFailures=Math.min(5,interstitialLoadFailures+1);
     final long delayMs=Math.min(180000L,15000L*(1L<<Math.min(interstitialLoadFailures-1,4)));
     nextInterstitialRetryAt=android.os.SystemClock.elapsedRealtime()+delayMs;
     android.util.Log.w("LazosAds","Interstitial load failed, code="+error.getCode()+", retry in ms="+delayMs);
     // Avoid rapid no-fill polling; never interrupt content to display a late ad.
     mainHandler.postDelayed(()->loadInterstitial(),delayMs);
    }
   });
 }'''
change(old,new,"interstitial loader")
p.write_text(s,encoding="utf-8")
gpath=Path("app/build.gradle")
g=gpath.read_text()
assert g.count('versionCode 18')==1
assert g.count("versionName '2.2.7'")==1
g=g.replace("versionCode 18","versionCode 19").replace("versionName '2.2.7'","versionName '2.2.8'")
assert "minSdk 19" in g and "targetSdk 36" in g and "play-services-ads:22.6.0" in g
gpath.write_text(g)
print("v2.2.8 code 19: interstitial retry/backoff, cache expiry and load guard, no added placements.")
