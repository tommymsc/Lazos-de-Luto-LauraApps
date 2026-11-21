# Lazos de Luto release R8 rules.
#
# Android Gradle Plugin and the Google Mobile Ads / UMP SDKs include their
# required consumer keep rules. Avoid broad -keep rules: they would disable
# obfuscation and prevent meeting Play's optimization targets.
#
# If a future release adds reflective or JNI-backed code, add narrowly scoped
# keep rules only for those classes after verifying a production test build.
