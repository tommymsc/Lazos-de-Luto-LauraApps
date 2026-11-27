#!/usr/bin/env python3
"""2.3.7: reduce unused ad requests, adaptive visible banners, conservative R8."""
from pathlib import Path
p=Path("app/src/main/java/gratis/lazosdeluto/MainActivity.java")
s=p.read_text(encoding="utf-8")
def change(a,b):
 global s
 assert s.count(a)==1,(a,s.count(a))
 s=s.replace(a,b,1)

# Do not preload fullscreen ads at every startup or during cooldown.
# Begin preloading only after actual category engagement and near eligibility.
change(" private boolean adsInitializing=false, adsInitialized=false, adsForeground=false, bannerLoaded=false;",
""" private boolean adsInitializing=false, adsInitialized=false, adsForeground=false, bannerLoaded=false;
 private boolean bannerLoading=false;
 private long bannerRetryAt=0L;
 private int bannerWidthDp=0;
 private final Runnable interstitialWarmup=()->loadInterstitial();
 private boolean interstitialOpportunity(){
  long now=android.os.SystemClock.elapsedRealtime();
  return previousCategory!=0 && !openingScreen &&
      now-adsSessionStartedAt>=45000L &&
      (lastFullscreenAt==0L || now-lastFullscreenAt>=CATEGORY_AD_COOLDOWN_MS-15000L);
 }
 private void scheduleInterstitial(){
  mainHandler.removeCallbacks(interstitialWarmup);
  if(!adsUsable() || openingScreen || previousCategory==0 || interstitial!=null || interstitialLoading || fullScreenActive)return;
  long now=android.os.SystemClock.elapsedRealtime();
  long wait=Math.max(0L,45000L-(now-adsSessionStartedAt));
  if(lastFullscreenAt!=0L)wait=Math.max(wait,CATEGORY_AD_COOLDOWN_MS-15000L-(now-lastFullscreenAt));
  wait=Math.max(wait,nextInterstitialRetryAt-now);
  mainHandler.postDelayed(interstitialWarmup,Math.max(0L,wait));
 }
""")
change("  adsForeground=true;\n  if(adsInitialized)loadAdFormats();","  adsForeground=true;\n  if(ad!=null)ad.resume();\n  if(adsInitialized)loadAdFormats();")
change("  adsForeground=false;\n  super.onPause();","  adsForeground=false;\n  mainHandler.removeCallbacks(interstitialWarmup);\n  if(ad!=null)ad.pause();\n  super.onPause();")
change("if(interstitial==null)loadInterstitial();","if(interstitial==null)scheduleInterstitial();")
change("fullScreenActive=false;navigate.run();loadInterstitial();","fullScreenActive=false;navigate.run();scheduleInterstitial();") if s.count("fullScreenActive=false;navigate.run();loadInterstitial();")==1 else None
s=s.replace("fullScreenActive=false;navigate.run();loadInterstitial();","fullScreenActive=false;navigate.run();scheduleInterstitial();")
# Keep the existing 6.5s maximum startup gate, never delay interactive content
# to force an ad. Prefer prior consent when eligible, still refresh UMP below.
change("  initAds();","  initAds();") if s.count("  initAds();")==1 else None
change("    if(!adsAllowed() || !openingScreen || !adsForeground)return;",
"""    if(!adsAllowed() || !openingScreen || !adsForeground){auditAd("App Open loaded outside eligible startup window");return;}""")
change("  showHome();\n }\n private void loadAppOpen(){","  showHome();\n  if(adsUsable())loadAdFormats();\n }\n private void loadAppOpen(){")
# Only request banner once the actual bottom dock exists. Use anchored adaptive
# size and reuse the view across screens; avoid background and splash requests.
start=s.index("  if(ad==null && !BuildConfig.BANNER_ID.isEmpty()){",s.index(" private void loadAdFormats(){"))
end=s.index("\n private void loadInterstitial(){",start)
s=s[:start]+"""  if(openingScreen){loadAppOpen();return;}
  if(bannerDock!=null && !BuildConfig.BANNER_ID.isEmpty())requestVisibleBanner();
  scheduleInterstitial();
 }
 private void requestVisibleBanner(){
  if(!adsUsable() || openingScreen || bannerDock==null || fullScreenActive)return;
  android.widget.FrameLayout dock=bannerDock;
  dock.post(()->{
   if(dock!=bannerDock || !adsUsable() || openingScreen || fullScreenActive || !dock.isAttachedToWindow())return;
   int pixels=dock.getWidth();
   if(pixels<=0 && dock.getParent() instanceof android.view.View)pixels=((android.view.View)dock.getParent()).getWidth();
   if(pixels<=0)return;
   int width=Math.max(1,(int)(pixels/getResources().getDisplayMetrics().density));
   if(ad!=null && bannerWidthDp!=width){
    ad.destroy();ad=null;bannerLoaded=false;bannerLoading=false;bannerRetryAt=0L;
   }
   if(ad==null){
    bannerWidthDp=width;
    ad=new AdView(this);
    ad.setAdUnitId(BuildConfig.BANNER_ID);
    ad.setAdSize(AdSize.getCurrentOrientationAnchoredAdaptiveBannerAdSize(this,width));
    final AdView candidate=ad;
    ad.setAdListener(new AdListener(){
     @Override public void onAdLoaded(){
      if(ad!=candidate)return;
      bannerLoading=false;bannerLoaded=true;bannerRetryAt=0L;
      if(adsUsable()&&!openingScreen)attachAd();
      auditAd("Banner loaded");
     }
     @Override public void onAdImpression(){auditAd("Banner impression");}
     @Override public void onAdFailedToLoad(LoadAdError error){
      if(ad!=candidate)return;
      bannerLoading=false;
      bannerRetryAt=android.os.SystemClock.elapsedRealtime()+60000L;
      auditAd("Banner load failed "+error.getCode());
      if(!bannerLoaded && bannerDock!=null)bannerDock.setVisibility(android.view.View.GONE);
      // SDK-managed refresh owns loaded banners; retry only an initial failure.
      if(!bannerLoaded)mainHandler.postDelayed(()->requestVisibleBanner(),60000L);
     }
    });
   }
   if(bannerLoaded){attachAd();return;}
   if(bannerLoading || android.os.SystemClock.elapsedRealtime()<bannerRetryAt)return;
   bannerLoading=true;
   auditAd("Banner request");
   ad.loadAd(new AdRequest.Builder().build());
  });
 }
"""+s[end:]
change("if(!adsUsable() || BuildConfig.INTERSTITIAL_ID.isEmpty() || isFinishing() || isDestroyed()",
       "if(!adsUsable() || !interstitialOpportunity() || BuildConfig.INTERSTITIAL_ID.isEmpty() || isFinishing() || isDestroyed()")
change("mainHandler.postDelayed(()->loadInterstitial(),delayMs);","scheduleInterstitial();")
# Ensure a new screen can request a banner even when the previous dock was gone.
change("if(ad==null || !bannerLoaded || bannerDock==null || openingScreen || !adsAllowed())return;",
"""if(bannerDock==null || openingScreen || !adsAllowed())return;
  if(ad==null || !bannerLoaded){if(adsUsable())requestVisibleBanner();return;}
  if(ad.getParent()==bannerDock){bannerDock.setVisibility(android.view.View.VISIBLE);return;}""")
p.write_text(s,encoding="utf-8")
gpath=Path("app/build.gradle")
g=gpath.read_text(encoding="utf-8")
assert g.count("versionCode 27")==1 and g.count("versionName '2.3.6'")==1
assert g.count("minifyEnabled false; shrinkResources false;")==1
g=g.replace("versionCode 27","versionCode 28",1).replace("versionName '2.3.6'","versionName '2.3.7'",1)
# Keep the SDK and startup hotfix, use conservative R8: obfuscation + shrinking,
# no optimizer transformations until the release startup has been validated.
g=g.replace("minifyEnabled false; shrinkResources false;","minifyEnabled true; shrinkResources true;",1)
gpath.write_text(g,encoding="utf-8")
rules=Path("app/proguard-rules.pro")
rules.write_text(rules.read_text(encoding="utf-8")+"\n# Conservative R8: retain obfuscation and shrinking, avoid optimizer rewrites.\n-dontoptimize\n",encoding="utf-8")
assert "minSdk 23" in g and "targetSdk 36" in g
assert "getCurrentOrientationAnchoredAdaptiveBannerAdSize" in s
assert "interstitialOpportunity()" in s
print("2.3.7 code28: adaptive banner, engagement-aware interstitial requests, conservative R8 obfuscation")
