# Lazos de Luto 2.2.3 versionCode14 (API 19+)

This is an alternative Android 4.4+ build intended to address Google Play loss of 2,214 devices.
It uses minSdk19, targetSdk36, 50 genuine JPGs and preserves messages/features.

**Monetization tradeoff**: AdMob Mobile Ads SDK 22.6.0 is sunset as of 2026-06-30, meaning ad serving is at risk. Newer Google Mobile Ads SDK v25.5.0 requires API24; the full Android 4.4+ single bundle cannot use it. UMP SDK2.2.0 and AndroidX Core1.12.0 support API19. The release is signed with the existing Play upload key and the workflow verifies its signature and assets. Play may still show reduced device coverage due to non-API factors and review policies.
