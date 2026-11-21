#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 4 ]]; then
    printf '%s\n' 'Usage: package-macos.sh SOURCE_DIRECTORY BUILD_DIRECTORY MOLTENVK_DRIVER_DIRECTORY NEW_OUTPUT_APP' >&2
    exit 2
fi
source_directory="$(cd "$1" && pwd)"
build="$(cd "$2" && pwd)"
driver="$(cd "$3" && pwd)"
root="$(cd "$(dirname "$0")" && pwd)"
test -f "$driver/MoltenVK_icd.json"
test -f "$driver/libMoltenVK.dylib"
test ! -e "$4"
stage="$(mktemp -d "${TMPDIR:-/tmp}/chiaki-metal.XXXXXX")"
trap 'rm -rf "$stage"' EXIT
bundle="$stage/Chiaki-ng Metal.app"
ditto --norsrc --noextattr --noacl "$build/gui/chiaki.app" "$bundle"
icd="$bundle/Contents/Resources/vulkan/icd.d"
mkdir -p "$icd"
cp "$driver/MoltenVK_icd.json" "$driver/libMoltenVK.dylib" "$icd/"
# SDL2-compat loads SDL3 at runtime. macdeployqt cannot infer this dependency.
cp -L "$(brew --prefix sdl3)/lib/libSDL3.dylib" "$bundle/Contents/MacOS/libSDL3.dylib"
chmod u+rw,go+r "$bundle/Contents/MacOS/libSDL3.dylib"

deploy="$(brew --prefix qt@6)/bin/macdeployqt"
if [[ ! -x "$deploy" ]]; then
    deploy="$(command -v macdeployqt)"
fi
"$deploy" "$bundle" \
    "-qmldir=$source_directory/gui/src/qml" "-libpath=$(brew --prefix)/lib" -no-codesign
python3 "$root/verify-macos-linkage.py" "$bundle" --relocate
python3 "$root/set-macos-metadata.py" "$bundle"
codesign --force --deep --sign - --entitlements "$source_directory/gui/entitlements.xml" "$bundle"
codesign --verify --deep --strict "$bundle"
ditto --norsrc --noextattr --noacl "$bundle" "$4"
xattr -dr com.apple.FinderInfo "$4" 2>/dev/null || true
xattr -dr com.apple.ResourceFork "$4" 2>/dev/null || true
codesign --verify --deep --strict "$4"
