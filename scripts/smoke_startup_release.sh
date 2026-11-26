#!/usr/bin/env bash
set -euo pipefail
pkg=lazosdeluto.gratis
apk=$(find app/build/outputs/apk/release -name '*.apk' | head -n 1)
test -s "$apk"
adb install -r "$apk"
adb shell pm clear "$pkg"
mkdir -p startup-smoke
# Emulators are recognized as test devices by Google Mobile Ads. Do not click ads.
for n in 1 2 3; do
  adb shell am force-stop "$pkg"
  adb logcat -c
  adb shell am start -W -n "$pkg/gratis.lazosdeluto.MainActivity" | tee "startup-smoke/launch-$n.txt"
  sleep 12
  adb logcat -d -b crash > "startup-smoke/crash-$n.txt"
  adb logcat -d -s LazosAds:D AndroidRuntime:E > "startup-smoke/ads-$n.txt"
  adb shell pidof "$pkg" | tee "startup-smoke/pid-$n.txt"
  test -s "startup-smoke/pid-$n.txt"
  if grep -Fq "$pkg" "startup-smoke/crash-$n.txt"; then
    cat "startup-smoke/crash-$n.txt"
    exit 1
  fi
  adb exec-out screencap -p > "startup-smoke/launch-$n.png"
done
echo 'PASS: release APK process survived three cold starts; no app crash in crash buffer.'
