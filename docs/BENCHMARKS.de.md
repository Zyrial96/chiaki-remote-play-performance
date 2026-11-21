# Messungen und Einordnung

[English](BENCHMARKS.md) · Deutsch · [Projektübersicht](../README.de.md)

| Vergleich | Messmethode | Ergebnis |
| --- | --- | --- |
| macOS, Übertragung über den Hauptspeicher gegenüber Metal-Import | CPU-Zeit für Bildvorbereitung und direkte Texturzuordnung während eines PS5-Streams bei 1080p60 auf einem M4 messen. | Die Summe beider Schritte sank im Mittel von 435,1 µs auf 88,3 µs. Der zuletzt installierte Testbuild importierte nach dem Warmlauf 6.518 aufeinanderfolgende gemessene Bilder. |
| macOS, zeitliche Abstände der Bildausgabe-Anfragen | Die Anfragen der App an Core Animation auswerten. Nach Abzug von Anlauf und Ende jeweils ein Zeitfenster von rund 18 Sekunden vergleichen. | Das 99. Perzentil der Abstände betrug 17,34 ms beim Kopierpfad und 17,23 ms beim Metal-Import. In beiden Fenstern lag kein Abstand über 25 ms. |
| Sony BRAVIA, Sofort gegenüber Ausgeglichen | Die Präsentationszeitstempel von SurfaceFlinger bei wiederholter Navigation im PS5-Menü auswerten. | 57,9 s bei 59,63 fps gegenüber 58,0 s bei 59,93 fps. Die Zahl der Bildabstände über 25 ms lag bei 18 gegenüber 1. Kein gemessener Abstand lag über 49 ms. |
| Xiaomi Android TV, Sofort gegenüber Ausgeglichen | Dasselbe SurfaceFlinger-Zeitstempelfeld während eines 1080p60-Streams auswerten. | Beide 44-Sekunden-Läufe erreichten im Mittel 59,94 fps und blieben ohne Bildabstand über 25 ms. Das galt auch für den 83,7 Sekunden langen Wiederholungstest mit Sofort. |

Core Animation erfasst in dieser Messung, wann die App die Bildausgabe **anfordert**. Wann die Pixel auf dem Panel sichtbar werden, bleibt offen. Die Android-Zeitstempel erfassen Abstände zwischen den Puffern, die an das Anzeigesystem übergeben werden. Die Zeit vom Controller bis zur Konsole ist darin nicht enthalten.

Die Messungen stammen aus kurzen LAN-Tests mit einer PS5. Je nach Bildausgabemodus können gleichmäßigere Abstände etwas zusätzliche Eingabeverzögerung kosten. Für Internetverbindungen, HDR, andere Geräte oder andere Spiele lassen sich daraus keine konkreten Werte ableiten.

P5M wurde separat als Vergleich für einen nativen Metal-Renderer getestet. Der macOS-Patch dieses Projekts nutzt den vorhandenen chiaki-ng-Renderer. P5M und seine Protokolländerungen gehören zum eigenständigen Vergleichsprojekt.
