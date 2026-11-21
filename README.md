# Chiaki Remote Play performance patches

English · [Deutsch](README.de.md)

Independent patches for [chiaki-ng on macOS](https://github.com/chiaki-ng/chiaki-ng) and the [Chiaki Android TV port](https://github.com/worstenbrood/chiaki-ng-androidtv). Both connect to an existing PlayStation console via Remote Play.

The project focuses on reducing the time a decoded frame spends waiting for display, keeping frame intervals consistent, and fixing device-specific playback failures.

## What changes

| Platform | Upstream base | Changes |
| --- | --- | --- |
| macOS | [chiaki-ng at `43728af`](https://github.com/chiaki-ng/chiaki-ng/tree/43728af2e639fecb8a7af1cd68c29820a40de973) | Import VideoToolbox surfaces as Metal textures into the existing libplacebo/Vulkan renderer. The renderer retains frames until it can safely recycle them and falls back to a software upload if the import fails. The patch also bounds frame handoff and corrects packet-loss accounting, audio recovery and a frame-queue lock error. |
| Android TV | [Android TV port at `8346914`](https://github.com/worstenbrood/chiaki-ng-androidtv/tree/8346914c4f00b739d41111239698f5c031097f1b) | Add **Immediate** and **Balanced** frame pacing, configure the codec for low latency where supported, handle trigger-only input devices, avoid stalls in audio input and align the native cryptography header across compilation units. |

On macOS the texture import requires the Vulkan renderer and direct frame mapping. On Android TV, **Immediate** sends the newest decoded frame available in a burst. **Balanced** waits for display refresh and keeps at most two decoded frames. The additional wait can improve cadence and can add some input latency.

## Measurements

- Apple Silicon M4, PS5 at 1080p60. Mean frame preparation and texture mapping fell from **0.435 ms to 0.088 ms** with the Metal import. A live run of the final build captured over **6,500** successful imports.
- Sony BRAVIA, PS5 at 1080p60. In two 58-second motion trials, gaps above 25 ms occurred **18 times in Immediate** and **once in Balanced**.
- Xiaomi Android TV, PS5 at 1080p60. Both modes sustained **59.94 fps** in 44-second trials with zero measured gaps above 25 ms. Immediate also passed an approximately 84-second run.

The measurements are specific to test hardware and scenes. They cover texture preparation or frame cadence. See [measurement methods and limitations](docs/BENCHMARKS.md) for the distinction from end-to-end input latency.

## Build and release

Published [macOS previews](https://github.com/Zyrial96/chiaki-remote-play-performance/releases) include the app, source archives and checksums. The preview requires Apple Silicon and macOS 27.2 or later. It uses an ad-hoc signature and carries no Apple notarization ticket.

- [Recreate the source and build either client](docs/BUILD.md)
- [Supported hardware, signing and release status](docs/RELEASE.md)

The two patches are licensed under the upstream terms. See [COPYING](COPYING) and [the OpenSSL exception](LICENSES/AGPL-3.0-only-OpenSSL.txt).

There is no affiliation with Sony Interactive Entertainment, PlayStation, or the upstream projects.
