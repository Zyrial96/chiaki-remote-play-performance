#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
if [[ $# -ne 2 ]]; then
    printf '%s\n' 'Usage: build-android.sh SOURCE_DIRECTORY armeabi-v7a|arm64-v8a' >&2
    exit 2
fi
case "$2" in
    armeabi-v7a|arm64-v8a) ;;
    *) exit 2 ;;
esac
: "${ANDROID_HOME:?Set ANDROID_HOME to the Android SDK}"
cd "$1"
bash gradlew --no-daemon -I "$root/scripts/unsigned-release.init.gradle" \
    "-Pabis=$2" testReleaseUnitTest assembleRelease
apk=app/build/outputs/apk/release/app-release-unsigned.apk
test -f "$apk"
"$ANDROID_HOME/build-tools/35.0.0/zipalign" -c -P 16 4 "$apk"
printf '%s\n' "$PWD/$apk"
