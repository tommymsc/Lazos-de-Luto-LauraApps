#!/usr/bin/env python3
"""Apply after v2.3.4; preserve UI, assets, IDs, signing and SDK compatibility."""
from pathlib import Path
p=Path("app/src/main/java/gratis/lazosdeluto/MainActivity.java")
s=p.read_text(encoding="utf-8")
def change(a,b):
 global s
 assert s.count(a)==1, (a,s.count(a))
 s=s.replace(a,b,1)
change(" private android.widget.FrameLayout bannerDock;", """ private android.widget.FrameLayout bannerDock;
 private boolean adsInitializing=false, adsInitialized=false, adsForeground=false, bannerLoaded=false;
 private long openingLoadedAt=0L, openingRetryAt=0L;
 private static final long OPEN_EXPIRY_MS=14400000L;
 private boolean adsAllowed(){
  return !isFinishing() && !isDestroyed() &&
      UserMessagingPlatform.getConsentInformation(this).canRequestAds();
 }
 private boolean adsUsable(){return adsInitialized && adsForeground && adsAllowed();}
 private void auditAd(String message){android.util.Log.d("LazosAds",message);}
 @Override protected void onResume(){
  super.onResume();
  adsForeground=true;
  if(adsInitialized)loadAdFormats();
 }
 @Override protected void onPause(){
  adsForeground=false;
  super.onPause();
 }
""")
change("if(ad==null || bannerDock==null || openingScreen || isFinishing() || isDestroyed())return;", "if(ad==null || !bannerLoaded || bannerDock==null || openingScreen || !adsAllowed())return;")
change("if(transition && now-adsSessionStartedAt>=60000L && interstitial!=null && !fullScreenActive && !isFinishing()", "if(transition && adsUsable() && now-adsSessionStartedAt>=60000L && interstitial!=null && !fullScreenActive && !isFinishing()")
change("now-lastFullscreenAt>=CATEGORY_AD_COOLDOWN_MS", "(lastFullscreenAt==0L || now-lastFullscreenAt>=CATEGORY_AD_COOLDOWN_MS)")
change("   adToShow.setFullScreenContentCallback(new FullScreenContentCallback(){", """   adToShow.setFullScreenContentCallback(new FullScreenContentCallback(){
    @Override public void onAdImpression(){auditAd("Interstitial impression");}""")
change("  openingAd=null;\n  showHome();","  showHome();")
start=s.index(" private void loadAppOpen(){")
end=s.index(" private void initAds(){",start)
s=s[:start]+""" private void loadAppOpen(){
  if(!adsUsable() || BuildConfig.APP_OPEN_ID.isEmpty() || openingLoading || fullScreenActive)return;
  long now=android.os.SystemClock.elapsedRealtime();
  if(openingAd!=null && now-openingLoadedAt>=OPEN_EXPIRY_MS){openingAd=null;openingLoadedAt=0L;}
  if(openingAd!=null || now<openingRetryAt)return;
  openingLoading=true;
  auditAd("App Open request");
  AppOpenAd.load(this,BuildConfig.APP_OPEN_ID,new AdRequest.Builder().build(),new AppOpenAdLoadCallback(){
   @Override public void onAdLoaded(AppOpenAd loaded){
    openingLoading=false;
    if(!adsAllowed())return;
    openingAd=loaded;openingLoadedAt=android.os.SystemClock.elapsedRealtime();
    auditAd("App Open loaded");
    // Never interrupt interactive content or show upon returning from sharing.
    if(!openingScreen || !adsUsable() || fullScreenActive)return;
    openingAd=null;openingLoadedAt=0L;fullScreenActive=true;
    loaded.setFullScreenContentCallback(new FullScreenContentCallback(){
     @Override public void onAdShowedFullScreenContent(){lastFullscreenAt=android.os.SystemClock.elapsedRealtime();auditAd("App Open shown");}
     @Override public void onAdImpression(){auditAd("App Open impression");}
     @Override public void onAdDismissedFullScreenContent(){fullScreenActive=false;finishOpeningScreen();loadAdFormats();}
     @Override public void onAdFailedToShowFullScreenContent(com.google.android.gms.ads.AdError error){auditAd("App Open show failed "+error.getCode());fullScreenActive=false;finishOpeningScreen();loadAdFormats();}
    });
    try{loaded.show(MainActivity.this);}catch(Exception error){auditAd("App Open show exception");fullScreenActive=false;finishOpeningScreen();loadAdFormats();}
   }
   @Override public void onAdFailedToLoad(LoadAdError error){
    openingLoading=false;openingRetryAt=android.os.SystemClock.elapsedRealtime()+60000L;
    auditAd("App Open load failed "+error.getCode());finishOpeningScreen();
   }
  });
 }
"""+s[end:]
change("  MobileAds.initialize(this,status->{});", """  if(!adsAllowed()){
   openingAd=null;interstitial=null;bannerLoaded=false;
   if(ad!=null){ad.destroy();ad=null;}
   if(bannerDock!=null)bannerDock.setVisibility(android.view.View.GONE);
   finishOpeningScreen();return;
  }
  if(!adsInitialized){
   if(adsInitializing)return;
   adsInitializing=true;
   MobileAds.initialize(this,status->runOnUiThread(()->{
    adsInitializing=false;adsInitialized=true;
    if(adsUsable())loadAdFormats();
   }));
   return;
  }
  if(!adsUsable())return;""")
change("     android.util.Log.d(\"LazosAds\",\"Banner loaded; attaching to visible bottom dock\");", """     if(!adsAllowed())return;
     bannerLoaded=true;
     android.util.Log.d("LazosAds","Banner loaded; attaching to visible bottom dock");""")
change("    @Override public void onAdFailedToLoad(LoadAdError error){\n     android.util.Log.w(\"LazosAds\",\"Banner load failed, code=\"+error.getCode());", """    @Override public void onAdImpression(){auditAd("Banner impression");}
    @Override public void onAdFailedToLoad(LoadAdError error){
     bannerLoaded=false;
     android.util.Log.w("LazosAds","Banner load failed, code="+error.getCode());""")
change("if(ad!=null && !isFinishing() && !isDestroyed()\n        && UserMessagingPlatform.getConsentInformation(MainActivity.this).canRequestAds()){", "if(ad!=null && adsUsable()){")
change("   ad.loadAd(new AdRequest.Builder().build());\n  }\n  loadInterstitial();\n  loadAppOpen();", """   auditAd("Banner request");
   ad.loadAd(new AdRequest.Builder().build());
  }else if(ad!=null && !bannerLoaded){
   // SDK refresh and bounded failure retry own subsequent requests.
  }
  // Opening takes priority; banner and interstitial remain independently available.
  loadAppOpen();
  loadInterstitial();""")
change("if(BuildConfig.INTERSTITIAL_ID.isEmpty() || isFinishing() || isDestroyed()", "if(!adsUsable() || BuildConfig.INTERSTITIAL_ID.isEmpty() || isFinishing() || isDestroyed()")
change("     interstitialLoading=false;\n     interstitialLoadFailures=0;", "     interstitialLoading=false;\n     if(!adsAllowed())return;\n     interstitialLoadFailures=0;")
change("  interstitialLoading=true;\n  InterstitialAd.load", "  interstitialLoading=true;\n  auditAd(\"Interstitial request\");\n  InterstitialAd.load")
change("  mainHandler.removeCallbacksAndMessages(null);", "  adsForeground=false;openingAd=null;interstitial=null;\n  mainHandler.removeCallbacksAndMessages(null);")
p.write_text(s,encoding="utf-8")
gpath=Path("app/build.gradle")
g=gpath.read_text(encoding="utf-8")
assert g.count("versionCode 25")==1 and g.count("versionName '2.3.4'")==1
gpath.write_text(g.replace("versionCode 25","versionCode 26",1).replace("versionName '2.3.4'","versionName '2.3.5'",1),encoding="utf-8")
print("2.3.5 code26: consent, initialization, foreground and impression diagnostics")
