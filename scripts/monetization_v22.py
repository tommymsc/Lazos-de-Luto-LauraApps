#!/usr/bin/env python3
"""Configure privacy-safe App Open / interstitial ad placements after upgrading UI."""
from pathlib import Path
p=Path("app/src/main/java/gratis/lazosdeluto/MainActivity.java")
s=p.read_text(encoding="utf-8")
assert 'showHome();initAds();' in s, "First apply scripts/upgrade_ui.py"
assert "private void initAds()" in s
s=s.replace('import com.google.android.gms.ads.interstitial.InterstitialAdLoadCallback;',
'''import com.google.android.gms.ads.interstitial.InterstitialAdLoadCallback;
import com.google.android.gms.ads.appopen.AppOpenAd;
import com.google.android.gms.ads.appopen.AppOpenAd.AppOpenAdLoadCallback;''')
s=s.replace('private int successfulSaves=0;',
'''private int successfulSaves=0;
 private int previousCategory=0;
 private long lastFullscreenAt=0L;
 private static final long CATEGORY_AD_COOLDOWN_MS=120000L;
 private AppOpenAd openingAd;
 private boolean openingScreen=false, fullScreenActive=false, openingLoading=false;
 private final android.os.Handler mainHandler=new android.os.Handler(android.os.Looper.getMainLooper());''')
s=s.replace('prefs=getSharedPreferences("favs",MODE_PRIVATE);showHome();initAds();',
'''prefs=getSharedPreferences("favs",MODE_PRIVATE);
  int launches=prefs.getInt("launch_count",0);
  prefs.edit().putInt("launch_count",launches+1).apply();
  if(launches>=2 && !BuildConfig.APP_OPEN_ID.isEmpty()){
   showOpeningScreen();
  }else{
   showHome();
  }
  initAds();''')
s=s.replace('cell.setOnClickListener(v->{style=idx+1;onlyFav=false;onlyPremium=false;page=0;showGallery();});',
'''cell.setOnClickListener(v->enterCategory(idx+1));''')
s=s.replace('new LinearLayout.LayoutParams(-1,dp(54)));','new LinearLayout.LayoutParams(-1,dp(54)));')
s=s.replace('Uri.parse("https://github.com/tommymsc/Lazos-de-Luto-LauraApps/blob/main/PRIVACIDAD.md")',
'Uri.parse("https://tommymsc.github.io/lazos-de-luto-privacy.html")')
# Remove saving-based interstitial, after an action should not be interrupting frequently
save_start=s.find('   successfulSaves++;')
save_end=s.find('\n  }catch(Exception e){',save_start)
assert save_start>=0 and save_end>save_start
s=s[:save_start]+s[save_end:]
# Replace ad lifecycle and loading methods
ad_start=s.index(' private void initAds(){')
s=s[:ad_start]+r'''
 private void enterCategory(int category){
  final boolean transition=previousCategory!=0 && previousCategory!=category;
  previousCategory=category;
  Runnable navigate=()->{style=category;onlyFav=false;onlyPremium=false;page=0;showGallery();};
  // A category transition is a natural content boundary. Do not block or delay if ad is absent.
  long now=android.os.SystemClock.elapsedRealtime();
  if(transition && interstitial!=null && !fullScreenActive
      && now-lastFullscreenAt>=CATEGORY_AD_COOLDOWN_MS){
   InterstitialAd adToShow=interstitial;interstitial=null;fullScreenActive=true;
   adToShow.setFullScreenContentCallback(new FullScreenContentCallback(){
    @Override public void onAdShowedFullScreenContent(){lastFullscreenAt=android.os.SystemClock.elapsedRealtime();}
    @Override public void onAdDismissedFullScreenContent(){fullScreenActive=false;navigate.run();loadInterstitial();}
    @Override public void onAdFailedToShowFullScreenContent(com.google.android.gms.ads.AdError err){fullScreenActive=false;navigate.run();loadInterstitial();}
   });
   try{adToShow.show(this);}catch(Exception ex){fullScreenActive=false;navigate.run();loadInterstitial();}
  }else{navigate.run();}
 }
 private void showOpeningScreen(){
  openingScreen=true;
  root=new LinearLayout(this);root.setOrientation(1);root.setGravity(Gravity.CENTER);
  root.setBackgroundColor(0xfff7f3f7);
  TextView t=label("Lazos de Luto\nPreparando tus recuerdos…",22);
  t.setGravity(Gravity.CENTER);root.addView(t);setContentView(root);
  // Never show an App Open ad after user has started interacting with content.
  mainHandler.postDelayed(()->finishOpeningScreen(),1700L);
 }
 private void finishOpeningScreen(){
  if(!openingScreen)return;
  openingScreen=false;
  showHome();
 }
 private void loadAppOpen(){
  if(BuildConfig.APP_OPEN_ID.isEmpty() || openingLoading || openingAd!=null || fullScreenActive)return;
  openingLoading=true;
  AppOpenAd.load(this,BuildConfig.APP_OPEN_ID,new AdRequest.Builder().build(),new AppOpenAdLoadCallback(){
   @Override public void onAdLoaded(AppOpenAd ad){
    openingLoading=false;openingAd=ad;
    if(openingScreen && !fullScreenActive){
      openingAd=null;fullScreenActive=true;
      ad.setFullScreenContentCallback(new FullScreenContentCallback(){
       @Override public void onAdShowedFullScreenContent(){lastFullscreenAt=android.os.SystemClock.elapsedRealtime();}
       @Override public void onAdDismissedFullScreenContent(){fullScreenActive=false;finishOpeningScreen();}
       @Override public void onAdFailedToShowFullScreenContent(com.google.android.gms.ads.AdError error){fullScreenActive=false;finishOpeningScreen();}
      });
      try{ad.show(MainActivity.this);}catch(Exception ignored){fullScreenActive=false;finishOpeningScreen();}
    }
   }
   @Override public void onAdFailedToLoad(LoadAdError err){openingLoading=false;finishOpeningScreen();}
  });
 }
 private void initAds(){
  ConsentRequestParameters params=new ConsentRequestParameters.Builder().build();
  UserMessagingPlatform.getConsentInformation(this).requestConsentInfoUpdate(this,params,()->{
   UserMessagingPlatform.loadAndShowConsentFormIfRequired(this,err->{
    if(UserMessagingPlatform.getConsentInformation(this).canRequestAds())loadAdFormats();
    else finishOpeningScreen();
   });
  },err->{
   if(UserMessagingPlatform.getConsentInformation(this).canRequestAds())loadAdFormats();
   else finishOpeningScreen();
  });
 }
 private void loadAdFormats(){
  MobileAds.initialize(this,status->{});
  if(ad==null && !BuildConfig.BANNER_ID.isEmpty()){
   ad=new AdView(this);
   ad.setAdUnitId(BuildConfig.BANNER_ID);
   ad.setAdSize(AdSize.BANNER);
   ad.loadAd(new AdRequest.Builder().build());
   if(!openingScreen)attachAd();
  }
  loadInterstitial();
  loadAppOpen();
 }
 private void loadInterstitial(){
  if(BuildConfig.INTERSTITIAL_ID.isEmpty() || interstitial!=null || fullScreenActive)return;
  InterstitialAd.load(this,BuildConfig.INTERSTITIAL_ID,new AdRequest.Builder().build(),
   new InterstitialAdLoadCallback(){
    @Override public void onAdLoaded(InterstitialAd newAd){interstitial=newAd;}
    @Override public void onAdFailedToLoad(LoadAdError error){interstitial=null;}
   });
 }
 @Override protected void onDestroy(){
  mainHandler.removeCallbacksAndMessages(null);
  if(ad!=null)ad.destroy();
  super.onDestroy();
 }
}
'''
# Avoid banner under splash; attachAd() called by each gallery/home navigation after splash.
p.write_text(s,encoding='utf-8')
assert 'enterCategory(idx+1)' in s and 'APP_OPEN_ID' in s
build=Path("app/build.gradle")
b=build.read_text(encoding="utf-8")
assert "INTERSTITIAL_ID" in b and "versionCode 10" in b
b=b.replace("versionCode 10","versionCode 11").replace("versionName '2.1.0'","versionName '2.2.0'")
b=b.replace("  debug { manifestPlaceholders.ADMOB_APP_ID",'''  debug { buildConfigField 'String','APP_OPEN_ID','"ca-app-pub-3940256099942544/9257395921"'; manifestPlaceholders.ADMOB_APP_ID''')
b=b.replace("  release { minifyEnabled false;",'''  release { buildConfigField 'String','APP_OPEN_ID', '"' + ((project.findProperty('LAZOS_ADMOB_OPEN_ID') ?: 'ca-app-pub-2506564165861733/9553696934').toString().matches('ca-app-pub-[0-9]{16}/[0-9]{10}') ? (project.findProperty('LAZOS_ADMOB_OPEN_ID') ?: 'ca-app-pub-2506564165861733/9553696934').toString() : '') + '"'; minifyEnabled false;''')
# Production defaults to the confirmed App Open ad unit; Gradle property can override it.
build.write_text(b,encoding="utf-8")
print('Configured v2.2.0 (11) AdMob ads; production App Open ID ready.')
