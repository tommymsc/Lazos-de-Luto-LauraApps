#!/usr/bin/env python3
"""Basic static checks of the release AAB. Real-device / Play Console validation is still required."""
import sys
import zipfile
from pathlib import Path

bundle=Path(sys.argv[1] if len(sys.argv)>1 else "app/build/outputs/bundle/release/app-release.aab")
assert bundle.is_file(), f"AAB not found: {bundle}"
with zipfile.ZipFile(bundle) as z:
    names=set(z.namelist())
    assert z.testzip() is None, "Corrupt entry in Android bundle"
    images=[n for n in names if n.startswith("base/assets/lazos/") and n.endswith(".jpg")]
    assert len(images)==50, f"Expected 50 mourning JPGs; found {len(images)}"
    assert len({z.read(n) for n in images})==50, "Found repeated JPEG payloads"
    assert "base/manifest/AndroidManifest.xml" in names, "Bundle missing AndroidManifest.xml"
    assert any(n.startswith("base/dex/") and n.endswith(".dex") for n in names), "Missing DEX classes"
    native=[n for n in names if n.endswith(".so")]
    if native:
        print("NOTICE: native libraries present; 16 KB compatibility needs verification:",native)
    else:
        print("No native .so libraries bundled.")
print(f"Verified bundle: {bundle} ({bundle.stat().st_size:,} bytes), 50 distinct JPEG images, manifest, DEX.")
