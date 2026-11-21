#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 2 ]]; then
    printf '%s\n' 'Usage: build-macos.sh SOURCE_DIRECTORY BUILD_DIRECTORY' >&2
    exit 2
fi
prefix="$(brew --prefix)"
ssl="$(brew --prefix openssl@3)"
ffmpeg="$(brew --prefix ffmpeg)"
qt="$(brew --prefix qt@6)"
protobuf="$(brew --prefix protobuf@29)"
sdl="$(brew --prefix sdl2-compat)"
source_directory="$(cd "$1" && pwd)"
mkdir -p "$2"
build="$(cd "$2" && pwd)"
python3 -m venv "$build/python"
"$build/python/bin/python" -m pip install --disable-pip-version-check 'protobuf==5.29.6'
mkdir -p "$build/openssl3-headers"
if [[ ! -e "$build/openssl3-headers/openssl" ]]; then
    ln -s "$ssl/include/openssl" "$build/openssl3-headers/openssl"
fi
cat > "$build/compiler-openssl3" <<'LAUNCHER'
#!/usr/bin/env bash
set -euo pipefail
compiler="$1"
shift
exec "$compiler" "-I$(dirname "$0")/openssl3-headers" "$@"
LAUNCHER
chmod +x "$build/compiler-openssl3"
export PATH="$build/python/bin:$protobuf/bin:$PATH"
export PKG_CONFIG_PATH="$sdl/lib/pkgconfig:$ssl/lib/pkgconfig${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}"
export CPATH="$ffmpeg/include${CPATH:+:$CPATH}"
cmake -S "$source_directory" -B "$build" -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCHIAKI_ENABLE_CLI=OFF -DCHIAKI_ENABLE_SETSU=OFF \
    -DCHIAKI_ENABLE_STEAMDECK_NATIVE=OFF -DCHIAKI_ENABLE_STEAM_SHORTCUT=OFF \
    -DCHIAKI_ENABLE_TESTS=ON -DCHIAKI_USE_SYSTEM_CURL=OFF \
    "-DCMAKE_PREFIX_PATH=$ssl;$prefix;$qt;$protobuf" \
    "-DOPENSSL_ROOT_DIR=$ssl" \
    "-DCMAKE_C_COMPILER_LAUNCHER=$build/compiler-openssl3" \
    "-DCMAKE_CXX_COMPILER_LAUNCHER=$build/compiler-openssl3" \
    "-DPython3_EXECUTABLE=$build/python/bin/python" "-DPYTHON_EXECUTABLE=$build/python/bin/python"
cmake --build "$build" --parallel "${BUILD_JOBS:-6}"
ctest --test-dir "$build" --output-on-failure
