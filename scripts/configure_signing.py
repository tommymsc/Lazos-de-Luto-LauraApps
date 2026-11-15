#!/usr/bin/env python3
"""Optional secure signing using GitHub Actions secrets. No key is stored in Git."""
from pathlib import Path
import os,base64,re
env=os.environ
required=("LAZOS_UPLOAD_KEYSTORE_BASE64","LAZOS_UPLOAD_KEYSTORE_PASSWORD","LAZOS_UPLOAD_KEY_ALIAS","LAZOS_UPLOAD_KEY_PASSWORD")
provided=[bool(env.get(k)) for k in required]
out=os.environ.get("GITHUB_OUTPUT")
def output(value):
 if out:
  with open(out,"a",encoding="utf8") as f:f.write("signed="+str(value).lower()+"\n")
if not any(provided):
 print("No upload key secrets configured; release AAB will be UNSIGNED and is NOT uploadable to Play.")
 output(False)
else:
 if not all(provided):raise SystemExit("Incomplete signing secrets: configure all four.")
 ks=Path("/tmp/lazos-upload-key.jks")
 ks.write_bytes(base64.b64decode(env["LAZOS_UPLOAD_KEYSTORE_BASE64"],validate=True))
 if ks.stat().st_size<500:raise SystemExit("Invalid keystore (too small)")
 os.chmod(ks,0o600)
 b=Path("app/build.gradle")
 s=b.read_text()
 assert "signingConfig signingConfigs.release" not in s
 signing="""
 signingConfigs {
  release {
   storeFile file('/tmp/lazos-upload-key.jks')
   storePassword System.getenv('LAZOS_UPLOAD_KEYSTORE_PASSWORD')
   keyAlias System.getenv('LAZOS_UPLOAD_KEY_ALIAS')
   keyPassword System.getenv('LAZOS_UPLOAD_KEY_PASSWORD')
  }
 }
 """
 s=s.replace(" buildTypes {",signing+"\n buildTypes {",1)
 s=s.replace("  release { buildConfigField", "  release { signingConfig signingConfigs.release; buildConfigField",1)
 b.write_text(s)
 print("Release signing configured via ephemeral keystore.")
 output(True)
