#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
if [[ $# -ne 2 ]]; then
    printf '%s\n' 'Usage: prepare-source.sh macos|android-tv NEW_SOURCE_DIRECTORY' >&2
    exit 2
fi
case "$1" in
    macos)
        upstream=https://github.com/chiaki-ng/chiaki-ng.git
        revision=43728af2e639fecb8a7af1cd68c29820a40de973
        printf -v patch '%s' "$root/patches/macos.patch"
        ;;
    android-tv)
        upstream=https://github.com/worstenbrood/chiaki-ng-androidtv.git
        revision=8346914c4f00b739d41111239698f5c031097f1b
        printf -v patch '%s' "$root/patches/android-tv.patch"
        ;;
    *) exit 2 ;;
esac
if [[ -e "$2" ]]; then
    printf 'Source directory already exists: %s\n' "$2" >&2
    exit 1
fi
git init -q "$2"
git -C "$2" remote add origin "$upstream"
git -C "$2" fetch --depth=1 origin "$revision"
git -C "$2" switch --detach FETCH_HEAD
git -C "$2" submodule update --init --recursive --jobs 4
git -C "$2" apply --cached --check "$patch"
git -C "$2" apply --check "$patch"
git -C "$2" apply "$patch"
git -C "$2" add -A
git -C "$2" diff --cached --check
