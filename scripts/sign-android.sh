#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 4 ]]; then
    printf '%s\n' 'Usage: sign-android.sh UNSIGNED_APK KEYSTORE ALIAS NEW_SIGNED_APK' >&2
    exit 2
fi
: "${ANDROID_BUILD_TOOLS:?Set ANDROID_BUILD_TOOLS to the Android SDK Build Tools directory}"
: "${ANDROID_SIGNING_PASSWORD_FILE:?Set ANDROID_SIGNING_PASSWORD_FILE to an owner-readable password file}"
test -f "$1"
test -f "$2"
test -r "$ANDROID_SIGNING_PASSWORD_FILE"
test ! -e "$4"
signer="$ANDROID_BUILD_TOOLS/apksigner"
aligner="$ANDROID_BUILD_TOOLS/zipalign"
test -x "$signer"
test -x "$aligner"
"$aligner" -c -P 16 4 "$1"
if "$signer" verify "$1" >/dev/null 2>&1; then
    printf '%s\n' 'Input APK already has a signature.' >&2
    exit 1
fi
umask 077
dir="$(mktemp -d "$(dirname "$4")/.apk-signing.XXXXXX")"
temp="$dir/signed.apk"
cleanup() {
    if [[ -f "$temp" ]]; then
        rm -- "$temp"
    fi
    rmdir -- "$dir"
}
trap cleanup EXIT
"$signer" sign --ks "$2" --ks-key-alias "$3" \
    --ks-pass "file:$ANDROID_SIGNING_PASSWORD_FILE" \
    --v4-signing-enabled false --out "$temp" "$1"
"$signer" verify --verbose --print-certs "$temp"
"$aligner" -c -P 16 4 "$temp"
ln "$temp" "$4"
