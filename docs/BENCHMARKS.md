# Measurements and interpretation

English · [Deutsch](BENCHMARKS.de.md)

| Comparison | Method | Result |
| --- | --- | --- |
| macOS CPU transfer and upload vs Metal import | On an M4, measure the CPU time for frame preparation and direct texture mapping during a 1080p60 PS5 stream. | Mean sum of stage times 435.1 µs vs 88.3 µs. Final installed test build imported 6,518 consecutive measured frames after warm-up. |
| macOS presentation requests | Core Animation requests from the app. Compare approximate 18-second windows after trimming startup and shutdown. | p99 spacing 17.34 ms for copy and 17.23 ms for the final Metal build. Neither of these two windows had a request gap above 25 ms. |
| Sony BRAVIA, Immediate vs Balanced | Use SurfaceFlinger presentation timestamps while repeatedly navigating the PS5 menu. | 57.9 s and 59.63 fps vs 58.0 s and 59.93 fps. Gaps above 25 ms were 18 vs 1. No measured gap exceeded 49 ms. |
| Xiaomi Android TV, Immediate vs Balanced | Use the same SurfaceFlinger timestamp field during a 1080p60 stream. | Both 44-second runs averaged 59.94 fps with zero gaps above 25 ms. A repeat of Immediate lasted 83.7 seconds and also had zero such gaps. |

The Core Animation timestamps mark presentation **requests**. They do not establish panel scan-out time. Android presentation timestamps show gaps between buffers presented to the display system. They do not include the controller-to-console path. These tests used one PS5 and short LAN runs. A change in frame pacing can trade response time for smoother delivery. The results are not estimates for WAN use, HDR, other devices, or every game.

P5M was evaluated independently as a native Metal comparison. Its application, modified code, binaries and protocol changes are outside this project. The macOS patch uses the existing chiaki-ng renderer.
