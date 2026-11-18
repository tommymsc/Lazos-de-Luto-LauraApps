# Lazos de Luto 2.2.2 (versionCode 13)

New code 13 because Play consumes previously uploaded version codes even if the draft is discarded. Android 7.0 API 24 minimum because Google Mobile Ads SDK 25.5.0 requires API 24. Target API 36. The Android 7–9 legacy storage path requests WRITE_EXTERNAL_STORAGE only on API 28 or below; Android 10+ uses scoped MediaStore. The bundle includes 50 unique memorial JPGs and 48 consoling messages. Signing uses protected GitHub secrets and verifies the public certificate and jarsigner signature.

To retain Android 4.4–6.x devices, attempt to include existing versionCode 8 as a retained legacy artifact in Play's `Actualización anterior > No incluidos > Incluir`. The legacy bundle is not included in the new AAB 13 and Google Play may reject retaining it because of its previous policy status or old API target. Do not claim old Android support without Play approving this configuration.
