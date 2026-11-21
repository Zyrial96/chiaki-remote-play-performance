# Freigabestatus und Signierung

[English](RELEASE.md) · Deutsch · [Projektübersicht](../README.de.md)

Die Pakete dieses Stands sind Release-Kandidaten. Die Mac-Vorschau ist für Apple Silicon gebaut, setzt macOS 27.2 voraus und trägt eine lokale Ad-hoc-Signatur. Gatekeeper hat sie bei der regulären Verteilungsprüfung abgelehnt. Der Android-TV-Kandidat verwendet die Paket-ID `com.chiaking.tv`. Die Mac-Vorschau übernimmt die Bundle-ID des Ausgangsprojekts und kann dessen Einstellungen verwenden.

| Paket | Geprüft | Vor allgemeiner Binärverteilung |
| --- | --- | --- |
| macOS Apple Silicon | Frischer Quellcode-Build und beide CTest-Suiten auf einem M4 bestanden. Die aus der Release-ZIP entpackte App importierte bei 1080p60 in 16 Sekunden 919 Bilder aus einem laufenden PS5-Stream. | Mit der Developer ID des Herausgebers signieren und von Apple notarisieren lassen. Das Notarisierungsticket an die App heften, Gatekeeper prüfen und das signierte Paket entpackt auf einem zweiten Mac mit der angegebenen Mindestversion testen. |
| Android TV `armeabi-v7a` | Build, 60 Unit-Tests, APK-Ausrichtung und Live-Streaming im LAN mit dem entwicklungssignierten Gegenstück auf Sony und Xiaomi. Die DEX-Dateien und nativen Bibliotheken stimmen bytegenau mit dem getesteten APK überein. | Mit dem dauerhaften Release-Schlüssel des Herausgebers signieren, Signatur prüfen und eine Neuinstallation testen. |
| Android TV `arm64-v8a` | Build, APK-Ausrichtung und 16-KiB-Ausrichtung der ARM64-ELF-Segmente geprüft. | Das signierte Paket auf einem physischen ARM64-Android-TV-Gerät testen, bevor die Gerätekompatibilität zugesichert wird. |

Android prüft die Signatur beim Update. Ein Paket mit einem anderen Signaturschlüssel kann eine bereits installierte App mit derselben Paket-ID nicht ersetzen. Prüfe eine Neuinstallation auf einem separaten Gerät oder in einem separaten Profil, damit vorhandene Einstellungen erhalten bleiben. Lege vor der ersten signierten Veröffentlichung die öffentliche Paket-ID und die Versionsregeln fest.

Signaturschlüssel, Entwicklerkennwörter und Registrierungsdaten gehören außerhalb des Repositorys. [Android-Dokumentation zur App-Signierung](https://developer.android.com/studio/publish/app-signing) · [Apple-Dokumentation zur Notarisierung](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution)

Veröffentliche zu den freigegebenen Dateien die exakten Quellarchive, die Build-Anleitung und die SHA-256-Prüfsummen. Bewahre die Upstream-Lizenzhinweise auf und stelle den zugehörigen Quellcode der mitgelieferten Komponenten entsprechend ihren Lizenzbedingungen bereit. [AGPL-Anforderungen an den zugehörigen Quellcode](https://www.gnu.org/licenses/agpl-3.0.en.html#section6) · [Upstream-Build-Rezept für macOS](https://github.com/chiaki-ng/chiaki-ng/blob/43728af2e639fecb8a7af1cd68c29820a40de973/.github/workflows/build-macos-arm.yml)
