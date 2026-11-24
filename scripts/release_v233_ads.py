#!/usr/bin/env python3
"""Lazos 2.3.3 code24: improve genuine viewability, do not manufacture impressions.
Run after release_v232_edge.py. Keep GMA, UMP, R8, target SDK and package intact.
"""
from pathlib import Path
p = Path("app/src/main/java/gratis/lazosdeluto/MainActivity.java")
s = p.read_text(encoding="utf-8")
def change(old, new, description):
    global s
    count = s.count(old)
    if count != 1:
        raise SystemExit(f"{description}: expected one anchor, found {count}")
    s = s.replace(old, new, 1)

# The existing bottom banner lives inside ScrollView. The view often never
# becomes visible because a visitor does not scroll to the bottom of a gallery.
# Reserve a dedicated dock OUTSIDE the content scroll area.
change("public class MainActivity extends Activity {",
       "public class MainActivity extends Activity {\n private android.widget.FrameLayout bannerDock;\n"
       " private final long adsSessionStartedAt=android.os.SystemClock.elapsedRealtime();",
       "banner dock and session state")
old = """  safeArea.addView(content, new android.widget.FrameLayout.LayoutParams(
      android.view.ViewGroup.LayoutParams.MATCH_PARENT,
      android.view.ViewGroup.LayoutParams.MATCH_PARENT));"""
new = """  android.widget.LinearLayout vertical = new android.widget.LinearLayout(this);
  vertical.setOrientation(android.widget.LinearLayout.VERTICAL);
  vertical.addView(content, new android.widget.LinearLayout.LayoutParams(
      android.view.ViewGroup.LayoutParams.MATCH_PARENT, 0, 1));
  bannerDock = new android.widget.FrameLayout(this);
  bannerDock.setVisibility(android.view.View.GONE);
  vertical.addView(bannerDock, new android.widget.LinearLayout.LayoutParams(
      android.view.ViewGroup.LayoutParams.MATCH_PARENT,
      android.view.ViewGroup.LayoutParams.WRAP_CONTENT));
  safeArea.addView(vertical, new android.widget.FrameLayout.LayoutParams(
      android.view.ViewGroup.LayoutParams.MATCH_PARENT,
      android.view.ViewGroup.LayoutParams.MATCH_PARENT));"""
change(old, new, "safe-area fixed banner dock")
change(""" private void attachAd(){
  if(ad!=null){if(ad.getParent() instanceof ViewGroup)((ViewGroup)ad.getParent()).removeView(ad);root.addView(ad);}
 }""",
""" private void attachAd(){
  // A loaded banner gets an independent bottom slot, never over gallery buttons.
  if(ad==null || bannerDock==null || openingScreen || isFinishing() || isDestroyed())return;
  if(ad.getParent() instanceof ViewGroup)((ViewGroup)ad.getParent()).removeView(ad);
  bannerDock.removeAllViews();
  android.widget.FrameLayout.LayoutParams params=new android.widget.FrameLayout.LayoutParams(
      android.view.ViewGroup.LayoutParams.WRAP_CONTENT,
      android.view.ViewGroup.LayoutParams.WRAP_CONTENT,android.view.Gravity.CENTER);
  bannerDock.addView(ad,params);
  bannerDock.setVisibility(android.view.View.VISIBLE);
 }""", "banner outside ScrollView")

# A nonloaded banner must not create empty space or require tapping/scrolling.
change("""   ad.setAdSize(AdSize.BANNER);
   ad.loadAd(new AdRequest.Builder().build());
   if(!openingScreen)attachAd();""",
"""   ad.setAdSize(AdSize.BANNER);
   ad.setAdListener(new AdListener(){
    @Override public void onAdLoaded(){
     android.util.Log.d("LazosAds","Banner loaded; attaching to visible bottom dock");
     if(!openingScreen)attachAd();
    }
    @Override public void onAdFailedToLoad(LoadAdError error){
     android.util.Log.w("LazosAds","Banner load failed, code="+error.getCode());
     if(bannerDock!=null)bannerDock.setVisibility(android.view.View.GONE);
     mainHandler.postDelayed(()->{
      if(ad!=null && !isFinishing() && !isDestroyed()
        && UserMessagingPlatform.getConsentInformation(MainActivity.this).canRequestAds()){
        ad.loadAd(new AdRequest.Builder().build());
      }
     },60000L);
    }
   });
   ad.loadAd(new AdRequest.Builder().build());""", "banner load callback and bounded retry")

# The old rule only triggered when switching between DIFFERENT categories.
# On this app visitors typically return home, then re-enter a category.
# A repeat visit to a category is a natural screen transition, too.
change("final boolean transition=previousCategory!=0 && previousCategory!=category;",
       "final boolean transition=previousCategory!=0;", "category navigation eligibility")
change("private static final long CATEGORY_AD_COOLDOWN_MS=120000L;",
       "private static final long CATEGORY_AD_COOLDOWN_MS=180000L;",
       "longer, safer full-screen cooldown")
change("if(transition && interstitial!=null && !fullScreenActive && !isFinishing()",
       "if(transition && now-adsSessionStartedAt>=60000L && interstitial!=null && !fullScreenActive && !isFinishing()",
       "first-minute interstitial guard")
# Avoid showing another full-screen ad quickly if the App Open was just shown.
# Existing lastFullscreenAt is shared with App Open and interstitial.
# The ad is consumed once and must be preloaded for a later navigation.

p.write_text(s, encoding="utf-8")

gpath = Path("app/build.gradle")
g = gpath.read_text(encoding="utf-8")
assert g.count("versionCode 23")==1 and g.count("versionName '2.3.2'")==1
for required in ("targetSdk 36","minSdk 23","play-services-ads:24.7.0",
                 "user-messaging-platform:3.2.0","minifyEnabled true","shrinkResources true"):
    assert required in g, required
g = g.replace("versionCode 23","versionCode 24",1).replace(
    "versionName '2.3.2'","versionName '2.3.3'",1)
gpath.write_text(g,encoding="utf-8")
assert 'root.addView(ad)' not in s
assert 'bannerDock.addView(ad' in s
assert 'now-adsSessionStartedAt>=60000L' in s
print("Lazos 2.3.3 code24: fixed bottom banner, load/retry, natural category boundary, 3m cooldown")
