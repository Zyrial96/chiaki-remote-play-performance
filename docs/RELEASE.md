# Release status and signing

English · [Deutsch](RELEASE.de.md)

Treat the packages associated with this snapshot as release candidates. The Mac artifact is Apple Silicon only, declares macOS 27.2 and is ad-hoc signed. Gatekeeper rejected the locally signed package under normal distribution assessment. The Android TV candidate uses package ID `com.chiaking.tv`. The Mac preview retains the upstream bundle ID and can share the upstream app's preferences.

| Artifact | Validation | Before general binary distribution |
| --- | --- | --- |
| macOS Apple Silicon | Fresh source build and both CTest suites passed on an M4. The app extracted from the release ZIP imported 919 live frames in 16 seconds at 1080p60. | Use the publisher's Developer ID, notarize and staple the distributable app, verify Gatekeeper, and test the signed archived artifact on a second Mac at the declared minimum macOS version. |
| Android TV `armeabi-v7a` | Build, 60 unit tests, APK alignment and live LAN playback with the development-signed equivalent on Sony and Xiaomi. The DEX files and native libraries are byte-identical to that tested APK. The local release signature has been verified. | Use the publisher's persistent release signing key, verify the signature and test a clean install. |
| Android TV `arm64-v8a` | Build, APK alignment and 16 KiB ARM64 ELF segment alignment. The locally signed APK passed clean installation, launch and reinstallation on an Android TV 14 ARM64 emulator. | Test the signed artifact on a physical ARM64 Android TV device before claiming compatibility. |

Android uses signing certificates to authorize updates. A package signed with a different key cannot replace an installed copy of the same package ID. Test the fresh-install route on a separate device or profile to preserve existing settings. Choose the public package ID and version policy before the first signed release.

[Signing scripts and instructions](SIGNING.md)

Use [Android app signing documentation](https://developer.android.com/studio/publish/app-signing) and [Apple's notarization instructions](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution). Keep signing identities, developer passwords and registration material outside the repository.

Attach the exact source archives, reproducible build instructions and SHA-256 checksums for the released files. This includes retaining upstream license notices and making the appropriate corresponding source available for bundled components. See the [AGPL source requirements](https://www.gnu.org/licenses/agpl-3.0.en.html#section6) and upstream [Mac build recipe](https://github.com/chiaki-ng/chiaki-ng/blob/43728af2e639fecb8a7af1cd68c29820a40de973/.github/workflows/build-macos-arm.yml).
