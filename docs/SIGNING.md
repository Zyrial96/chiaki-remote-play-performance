# Signing release candidates

English · [Deutsch](SIGNING.de.md) · [Project overview](../README.md)

## Android TV

Use the same private release key for every update of this package. Keep the PKCS#12 file and its password in separate, access-controlled storage. The script expects the key and keystore passwords to be the same. The password file must be readable only by the signing user.

```bash
export ANDROID_BUILD_TOOLS=/path/to/android-sdk/build-tools/35.0.0
export ANDROID_SIGNING_PASSWORD_FILE=/path/to/private/password-file
scripts/sign-android.sh unsigned.apk /path/to/release.p12 chiaki-tv-release signed.apk
```

The script checks ZIP alignment before and after signing and verifies the resulting certificate. Both local Android candidates were verified with APK signature schemes v2 and v3. Their unpacked application payloads match the corresponding unsigned builds byte for byte.

The package ID is `com.chiaking.tv`. Android only permits an update with the same authorized signer. Use a clean device or emulator to test the initial install if an existing copy uses a different signing certificate. See [Android's app signing documentation](https://developer.android.com/studio/publish/app-signing).

## macOS

Use a valid **Developer ID Application** identity and an existing `notarytool` Keychain profile. Supply the entitlements from the same prepared source tree used for the build.

```bash
python3 scripts/notarize-macos.py 'Chiaki-ng Metal.app' chiaki-ng-metal-notarized.zip \
  --identity 'Developer ID Application: NAME (TEAMID)' \
  --entitlements source-macos/gui/entitlements.xml \
  --notary-profile chiaki-release
```

The script signs the bundle with hardened runtime and a secure timestamp, submits it to Apple, staples the accepted ticket and runs Gatekeeper assessment before writing the output ZIP. A valid Developer ID identity was unavailable on the build Mac, so this release path was only checked through the credential preflight. See [Apple's notarization instructions](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution).
