# Chiaki Remote Play – Performance-Patches

[English](README.md) · Deutsch

Unabhängige Patches für [chiaki-ng unter macOS](https://github.com/chiaki-ng/chiaki-ng) und die [Android-TV-Portierung von Chiaki](https://github.com/worstenbrood/chiaki-ng-androidtv). Beide Clients verbinden sich per Remote Play mit einer vorhandenen PlayStation-Konsole.

Die Patches verkürzen die Verarbeitung dekodierter Bilder, verbessern je nach Gerät die Gleichmäßigkeit der Bildausgabe und beheben gerätespezifische Wiedergabefehler.

## Änderungen gegenüber den Ausgangsversionen

| Plattform | Ausgangsversion | Änderungen |
| --- | --- | --- |
| macOS | [chiaki-ng, Commit `43728af`](https://github.com/chiaki-ng/chiaki-ng/tree/43728af2e639fecb8a7af1cd68c29820a40de973) | Importiert VideoToolbox-Bildflächen als Metal-Texturen in den vorhandenen libplacebo/Vulkan-Renderer. Der Renderer hält die Bilder so lange vor, bis er sie sicher freigeben kann. Scheitert der Import, überträgt er das Bild über den Hauptspeicher. Der Patch begrenzt außerdem die Warteschlange bei der Bildübergabe und korrigiert Fehler bei der Erfassung von Paketverlusten, der Audiowiederherstellung und der Sperrlogik der Bildwarteschlange. |
| Android TV | [Android-TV-Port, Commit `8346914`](https://github.com/worstenbrood/chiaki-ng-androidtv/tree/8346914c4f00b739d41111239698f5c031097f1b) | Ergänzt die Bildausgabemodi **Sofort** und **Ausgeglichen**, aktiviert den Niedriglatenzmodus des Decoders, sofern er ihn unterstützt, und verbessert die Verarbeitung von Controllern, die Trigger als Tasten melden. Der Patch behebt außerdem Blockaden bei der Audioeingabe und vereinheitlicht den nativen Kryptografie-Header zwischen den Kompilierungseinheiten. |

Unter macOS benötigt der Texturimport den Vulkan-Renderer und die direkte Bildzuordnung. Unter Android TV gibt **Sofort** bei dicht aufeinanderfolgenden Bildern das neueste verfügbare dekodierte Bild aus. **Ausgeglichen** richtet die Ausgabe am Bildwiederholtakt aus und hält höchstens zwei dekodierte Bilder vor. Die zusätzliche Wartezeit kann die Bildabstände gleichmäßiger machen und die Eingabeverzögerung etwas erhöhen.

## Gemessene Ergebnisse

- **Mac mit Apple M4, PS5-Stream bei 1080p60.** Bildvorbereitung und Texturzuordnung dauerten mit Metal-Import im Mittel **0,088 ms** gegenüber **0,435 ms** bei der Übertragung über den Hauptspeicher. In einem Live-Test wurden über **6.500** Bilder erfolgreich importiert.
- **Sony BRAVIA, PS5-Stream bei 1080p60.** In zwei Bewegungstests von je rund 58 Sekunden gab es mit **Sofort** 18 Bildabstände über 25 ms, mit **Ausgeglichen** einen.
- **Xiaomi Android TV, PS5-Stream bei 1080p60.** Beide Modi erreichten in jeweils 44 Sekunden **59,94 fps**. Es gab keinen gemessenen Bildabstand über 25 ms. Mit **Sofort** blieb es auch in einem rund 84 Sekunden langen Wiederholungstest dabei.

Die Ergebnisse gelten für die getesteten Geräte und Szenen. Die [Messmethoden und Grenzen](docs/BENCHMARKS.de.md) erläutern, welche Teile der Verarbeitung erfasst wurden und wie sich diese Werte von der Eingabe-bis-Bildschirm-Latenz unterscheiden.

## Build und Freigabe

- [Quellstand wiederherstellen und Clients bauen](docs/BUILD.de.md)
- [Getestete Hardware, Signierung und Freigabestatus](docs/RELEASE.de.md)

Für die Patches gelten die Lizenzbedingungen der Ausgangsprojekte. Siehe [Lizenztext](COPYING) und [OpenSSL-Ausnahme](LICENSES/AGPL-3.0-only-OpenSSL.txt).

Das Projekt ist unabhängig von Sony Interactive Entertainment, PlayStation und den Ausgangsprojekten.
