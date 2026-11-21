# Clients aus dem Quellcode bauen

[English](BUILD.md) · Deutsch · [Projektübersicht](../README.de.md)

Führe die Befehle im Hauptverzeichnis dieses Projekts aus. Das Skript zur Quellvorbereitung lädt die festgelegte Upstream-Revision, initialisiert die Submodule mit ihren festgeschriebenen Revisionen und wendet den vollständigen Patch für den gewählten Client an. Das Zielverzeichnis darf noch nicht existieren.

## Android TV

Voraussetzungen sind JDK 17, Android SDK Platform 35, Build Tools 35.0.0, NDK 28.2.13676358 und Android SDK CMake 3.22.1. Außerdem werden Python 3 mit dem Protobuf-Modul, `protoc`, Perl, Git und die üblichen nativen Build-Werkzeuge benötigt. Setze `JAVA_HOME` und `ANDROID_HOME`. Der Gradle-Wrapper legt die Gradle-Version fest.

```bash
scripts/prepare-source.sh android-tv source-android
scripts/build-android.sh source-android armeabi-v7a
```

Das Skript führt die Android-Unit-Tests aus, erstellt ein unsigniertes Release-APK und prüft dessen ZIP-Ausrichtung. Die nativen Sanitizer-Tests laufen unter Linux mit `python3 source-android/native/tests/run_audio_decoder_input_test.py`. Sichere das erste APK unter einem eigenen Namen, bevor du denselben Build-Befehl mit `arm64-v8a` ausführst.

Android benötigt für die Installation ein signiertes APK. Der Build verwendet dafür absichtlich keinen Testschlüssel des Ausgangsprojekts.

## macOS

Voraussetzungen sind ein Mac mit Apple Silicon, die Xcode Command Line Tools, Homebrew und Python ab Version 3.9. Installiere `qt@6`, `ffmpeg`, `libplacebo`, `sdl3`, `sdl2-compat`, `openssl@3`, `protobuf@29`, `pkgconf`, `cmake`, `ninja`, `nasm`, `opus`, `speexdsp`, `json-c`, `miniupnpc` und `libevent`. Das Build-Skript installiert seine Python-Protobuf-Abhängigkeit in einer eigenen virtuellen Umgebung im Build-Verzeichnis.

```bash
scripts/prepare-source.sh macos source-macos
scripts/build-macos.sh source-macos build-macos
```

Die geprüfte Toolchain umfasste FFmpeg 9.0.2, libplacebo 7.387.0, OpenSSL 3.5.9, SDL2-compat 2.32.74, Protobuf 29.6, Ninja 1.13.2 und CMake 4.5.1. CTest führt die Build-Tests aus.

Lade für das App-Bundle das [macOS-Archiv von MoltenVK 1.4.2](https://github.com/KhronosGroup/MoltenVK/releases/tag/v1.4.2). Übergib den Ordner, der `MoltenVK_icd.json` und `libMoltenVK.dylib` enthält.

```bash
scripts/package-macos.sh source-macos build-macos path/to/moltenvk-driver '/private/tmp/Chiaki-ng Metal.app'
```

Verwende für das App-Bundle einen lokalen, nicht synchronisierten Ordner. Zusätzliche Dateisystem-Metadaten können die Signatur ungültig machen. Das Paketierungsskript bestimmt die macOS-Mindestversion aus den mitgelieferten Apple-Silicon-Binärdateien und signiert das Bundle für lokale Tests per Ad-hoc-Signatur. Die mitgelieferten Abhängigkeiten dieses Builds erfordern macOS 27.2. Geprüft wurde die lokale Verbindung zu einer PS5. Die PSN-Anmeldung hängt in diesem Build von der Verfügbarkeit von Qt WebEngine ab und wurde nicht geprüft.

## Quellarchive erstellen

```bash
python3 scripts/archive-source.py source-macos chiaki-macos-source.tar.gz
python3 scripts/archive-source.py source-android chiaki-android-tv-source.tar.gz
```

Die Archive enthalten den vorbereiteten Anwendungsquellcode und die exakt ausgecheckten Submodulrevisionen. Das Android-Archiv enthält keinen Upstream-Entwicklungsschlüssel. Stelle mit der Veröffentlichung auch die Patches, Build-Skripte, Drittanbieterhinweise und Verweise auf die jeweiligen Quellstände bereit. System-SDKs und separat installierte Build-Abhängigkeiten stehen in dieser Anleitung.
