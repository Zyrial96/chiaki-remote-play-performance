# Recreating the clients

English · [Deutsch](BUILD.de.md)

Run the commands from the root of this project. The source-preparation script checks out the exact upstream revision, initializes its pinned submodules and applies the full patch for the selected client. It expects a new directory.

## Android TV

Use JDK 17, Android SDK platform 35, Build Tools 35.0.0, NDK 28.2.13676358 and Android SDK CMake 3.22.1. Make Python 3 with its protobuf module, `protoc`, Perl, Git and the standard native build tools available. Set `JAVA_HOME` and `ANDROID_HOME`. The Gradle wrapper pins the Gradle version.

```bash
scripts/prepare-source.sh android-tv source-android
scripts/build-android.sh source-android armeabi-v7a
```

The script runs the Android unit tests, builds a release APK without a signing key and checks its ZIP alignment. On Linux, run the native sanitizer tests with `python3 source-android/native/tests/run_audio_decoder_input_test.py`. Copy the APK to a separate output name before building `arm64-v8a` using the same command with that ABI. Android requires a signed APK to install. The signing override deliberately excludes the upstream test signature.

## macOS

Use Apple Silicon, the Xcode command-line tools, Homebrew and Python 3.9 or newer. Install `qt@6`, `ffmpeg`, `libplacebo`, `sdl3`, `sdl2-compat`, `openssl@3`, `protobuf@29`, `pkgconf`, `cmake`, `ninja`, `nasm`, `opus`, `speexdsp`, `json-c`, `miniupnpc` and `libevent`. The build script installs its Python protobuf dependency in a build-local virtual environment.

```bash
scripts/prepare-source.sh macos source-macos
scripts/build-macos.sh source-macos build-macos
```

The validated toolchain included FFmpeg 9.0.2, libplacebo 7.387.0, OpenSSL 3.5.9, SDL2-compat 2.32.74, protobuf 29.6, Ninja 1.13.2 and CMake 4.5.1. The build tests are run by CTest.

To bundle the app for local testing, download the [MoltenVK 1.4.2 macOS archive](https://github.com/KhronosGroup/MoltenVK/releases/tag/v1.4.2) and pass the directory containing `MoltenVK_icd.json` and `libMoltenVK.dylib`.

```bash
scripts/package-macos.sh source-macos build-macos path/to/moltenvk-driver '/private/tmp/Chiaki-ng Metal.app'
```

Use a local, non-synced directory for the app bundle to avoid filesystem metadata invalidating the signature. The packaging script sets the minimum macOS version from the bundled Apple Silicon binaries and uses an ad-hoc signature. The bundled dependencies in this snapshot require macOS 27.2. The tested path is a local PS5 connection. PSN login in this build depends on availability of Qt WebEngine and has no validation here.

## Source archives

```bash
python3 scripts/archive-source.py source-macos chiaki-macos-source.tar.gz
python3 scripts/archive-source.py source-android chiaki-android-tv-source.tar.gz
```

The archives include the staged application source and the exact checked-out submodule revisions. The Android archive excludes the upstream development keystore. Keep the preparation patch, build scripts, third-party notices and source references alongside the release. System SDKs and separately installed build dependencies are documented here rather than embedded in the archives.
