#!/usr/bin/env python3
"""Prepare Lazos de Luto 2.3.2 (code 23): edge-to-edge with system insets.
Runs immediately after release_v231.py in CI; preserves AdMob, Fragment and R8.
"""
from pathlib import Path

gradle = Path("app/build.gradle")
g = gradle.read_text(encoding="utf-8")
assert g.count("versionCode 22") == 1 and g.count("versionName '2.3.1'") == 1
assert "minSdk 23" in g and "targetSdk 36" in g
assert "minifyEnabled true" in g and "shrinkResources true" in g
assert "play-services-ads:24.7.0" in g and "user-messaging-platform:3.2.0" in g
assert "strictly '1.9.1'" in g
g = g.replace("versionCode 22", "versionCode 23", 1)
g = g.replace("versionName '2.3.1'", "versionName '2.3.2'", 1)
# WindowCompat.enableEdgeToEdge requires androidx.core 1.17.0 or newer.
if "androidx.core:core:1.12.0" not in g:
    raise SystemExit("Unexpected androidx.core dependency; release aborted")
g = g.replace("androidx.core:core:1.12.0", "androidx.core:core:1.17.0", 1)
gradle.write_text(g, encoding="utf-8")

source = Path("app/src/main/java/gratis/lazosdeluto/MainActivity.java")
java = source.read_text(encoding="utf-8")
anchor = "public class MainActivity extends Activity {"
if java.count(anchor) != 1:
    raise SystemExit("MainActivity class marker missing")
insert = r"""
 // Apply modern edge-to-edge across all dynamically created screens.
 // The wrapper draws under the system bars; its content respects the insets.
 @Override public void setContentView(android.view.View content) {
  android.widget.FrameLayout safeArea = new android.widget.FrameLayout(this);
  safeArea.setBackgroundColor(0xfffaf8f8);
  safeArea.addView(content, new android.widget.FrameLayout.LayoutParams(
      android.view.ViewGroup.LayoutParams.MATCH_PARENT,
      android.view.ViewGroup.LayoutParams.MATCH_PARENT));
  androidx.core.view.ViewCompat.setOnApplyWindowInsetsListener(safeArea, (v, insets) -> {
   androidx.core.graphics.Insets bars = insets.getInsets(
       androidx.core.view.WindowInsetsCompat.Type.systemBars()
       | androidx.core.view.WindowInsetsCompat.Type.displayCutout());
   v.setPadding(bars.left, bars.top, bars.right, bars.bottom);
   return insets;
  });
  super.setContentView(safeArea);
  androidx.core.view.ViewCompat.requestApplyInsets(safeArea);
 }
 @Override protected void onPostCreate(android.os.Bundle savedInstanceState) {
  super.onPostCreate(savedInstanceState);
  androidx.core.view.WindowCompat.enableEdgeToEdge(getWindow());
 }
"""
java = java.replace(anchor, anchor + "\n" + insert, 1)
# No deprecated system bar color APIs or deprecated edge-to-edge opt-outs.
for deprecated in ("setStatusBarColor(", "setNavigationBarColor(",
                   "windowOptOutEdgeToEdgeEnforcement", "setSystemUiVisibility("):
    if deprecated in java:
        raise SystemExit(f"Deprecated window API still present: {deprecated}")
source.write_text(java, encoding="utf-8")
print("v2.3.2 code23: system-bar insets, edge-to-edge, core 1.17.0, R8 and AdMob retained.")
