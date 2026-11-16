#!/usr/bin/env python3
"""Configure Android signing with Actions secrets; verify uploaded public cert matches private key.
No keystore, password, or PEM is printed or added to Git.
"""
import base64
import hashlib
import os
import subprocess
import tempfile
from pathlib import Path

env = os.environ
required = (
    "LAZOS_UPLOAD_KEYSTORE_BASE64",
    "LAZOS_UPLOAD_KEYSTORE_PASSWORD",
    "LAZOS_UPLOAD_KEY_ALIAS",
    "LAZOS_UPLOAD_KEY_PASSWORD",
    "LAZOS_UPLOAD_CERT_PEM_BASE64",
)
present = [bool(env.get(k)) for k in required]
out = env.get("GITHUB_OUTPUT")

def set_signed(value):
    if out:
        with open(out, "a", encoding="utf-8") as f:
            f.write(f"signed={str(value).lower()}\n")

if not any(present):
    print("Signing secrets absent: generate unsigned AAB ONLY for inspection; never upload to Play.")
    set_signed(False)
else:
    if not all(present):
        raise SystemExit("Signing secrets partially configured; all five are required.")
    try:
        private_bytes = base64.b64decode(env["LAZOS_UPLOAD_KEYSTORE_BASE64"], validate=True)
        public_bytes = base64.b64decode(env["LAZOS_UPLOAD_CERT_PEM_BASE64"], validate=True)
    except Exception as exc:
        raise SystemExit("Invalid Base64 in signing secrets.") from exc
    if len(private_bytes) < 500 or b"BEGIN CERTIFICATE" not in public_bytes:
        raise SystemExit("Keystore or public certificate is invalid.")
    key_path = Path("/tmp/lazos-upload-key.jks")
    cert_path = Path("/tmp/lazos-upload-expected.pem")
    actual_path = Path("/tmp/lazos-upload-actual.pem")
    key_path.write_bytes(private_bytes)
    cert_path.write_bytes(public_bytes)
    os.chmod(key_path, 0o600)
    os.chmod(cert_path, 0o600)

    subprocess.run(
        ["keytool", "-exportcert", "-rfc", "-keystore", str(key_path),
         "-storepass:env", "LAZOS_UPLOAD_KEYSTORE_PASSWORD",
         "-alias", env["LAZOS_UPLOAD_KEY_ALIAS"], "-file", str(actual_path)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )

    def fingerprint(path):
        der = subprocess.check_output(
            ["openssl", "x509", "-in", str(path), "-outform", "DER"], stderr=subprocess.PIPE
        )
        return hashlib.sha256(der).hexdigest().upper()

    actual = fingerprint(actual_path)
    expected = fingerprint(cert_path)
    if actual != expected:
        raise SystemExit("The private keystore certificate DOES NOT MATCH the PEM sent to Play Console.")
    print("Upload key matches supplied public certificate. SHA-256:", ":".join(actual[i:i+2] for i in range(0,64,2)))
    build = Path("app/build.gradle")
    s = build.read_text(encoding="utf-8")
    if "signingConfig signingConfigs.release" in s:
        raise SystemExit("Signing configuration was already applied.")
    signing = """
 signingConfigs {
  release {
   storeFile file('/tmp/lazos-upload-key.jks')
   storePassword System.getenv('LAZOS_UPLOAD_KEYSTORE_PASSWORD')
   keyAlias System.getenv('LAZOS_UPLOAD_KEY_ALIAS')
   keyPassword System.getenv('LAZOS_UPLOAD_KEY_PASSWORD')
  }
 }
 """
    if " buildTypes {" not in s or "  release { buildConfigField" not in s:
        raise SystemExit("Unsupported Gradle build file; refusing to sign.")
    s = s.replace(" buildTypes {", signing + "\n buildTypes {", 1)
    s = s.replace("  release { buildConfigField", "  release { signingConfig signingConfigs.release; buildConfigField", 1)
    build.write_text(s, encoding="utf-8")
    set_signed(True)
    print("Release signing enabled without storing the private key in Git.")
