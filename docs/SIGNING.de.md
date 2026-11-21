# Release-Kandidaten signieren

[English](SIGNING.md) · Deutsch · [Projektübersicht](../README.de.md)

## Android TV

Verwende für alle Updates dieses Pakets denselben privaten Release-Schlüssel. Bewahre die PKCS#12-Datei und ihr Kennwort getrennt und zugriffsgeschützt auf. Das Skript erwartet dasselbe Kennwort für Schlüssel und Schlüsselspeicher. Die Kennwortdatei sollte nur für das signierende Benutzerkonto lesbar sein.

```bash
export ANDROID_BUILD_TOOLS=/pfad/zum/android-sdk/build-tools/35.0.0
export ANDROID_SIGNING_PASSWORD_FILE=/pfad/zur/privaten/kennwortdatei
scripts/sign-android.sh unsigned.apk /pfad/zu/release.p12 chiaki-tv-release signed.apk
```

Das Skript prüft die ZIP-Ausrichtung vor und nach dem Signieren sowie das Zertifikat des fertigen APKs. Beide lokalen Android-Kandidaten wurden mit den APK-Signaturverfahren v2 und v3 verifiziert. Ihr entpackter Anwendungsinhalt stimmt bytegenau mit den jeweiligen unsignierten Builds überein.

Die Paket-ID lautet `com.chiaking.tv`. Android erlaubt ein Update nur mit einem für das Paket zugelassenen Signierer. Verwende für den Neuinstallationstest ein separates Gerät oder einen Emulator, falls bereits eine Kopie mit anderem Signaturzertifikat installiert ist. [Android-Dokumentation zur App-Signierung](https://developer.android.com/studio/publish/app-signing)

## macOS

Voraussetzungen sind eine gültige **Developer ID Application** und ein vorhandenes `notarytool`-Profil im Schlüsselbund. Verwende die Entitlements aus demselben vorbereiteten Quellbaum, aus dem die App gebaut wurde.

```bash
python3 scripts/notarize-macos.py 'Chiaki-ng Metal.app' chiaki-ng-metal-notarized.zip \
  --identity 'Developer ID Application: NAME (TEAMID)' \
  --entitlements source-macos/gui/entitlements.xml \
  --notary-profile chiaki-release
```

Das Skript signiert das Bundle mit Hardened Runtime und einem sicheren Zeitstempel, reicht es bei Apple ein und heftet nach Annahme das Notarisierungsticket an. Vor dem Erstellen der ZIP-Datei prüft Gatekeeper das Bundle. Auf dem Build-Mac stand keine gültige Developer ID zur Verfügung. Deshalb ist dieser Freigabeweg bisher nur bis zur Prüfung der Signieridentität getestet. [Apple-Dokumentation zur Notarisierung](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution)
