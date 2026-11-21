#!/usr/bin/env python3
"""Sign a packaged Chiaki app with Developer ID and notarize its release ZIP."""

import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile


def run(*args):
    subprocess.run(args, check=True)


def capture(*args):
    return subprocess.check_output(args, text=True)


def signing_identity(identity):
    listing = capture("security", "find-identity", "-v", "-p", "codesigning")
    identities = re.findall(
        r'(?m)^\s*\d+\) ([0-9A-F]{40}) "(Developer ID Application: [^"]+)"',
        listing,
    )
    matches = [fingerprint for fingerprint, name in identities if identity in (fingerprint, name)]
    if len(matches) != 1:
        raise SystemExit("A matching, valid Developer ID Application identity is required.")
    return matches[0]


def is_macho(path):
    if not path.is_file() or path.is_symlink():
        return False
    with path.open("rb") as handle:
        return handle.read(4) in (
            b"\xcf\xfa\xed\xfe", b"\xfe\xed\xfa\xcf",
            b"\xca\xfe\xba\xbe", b"\xca\xfe\xba\xbf",
        )


def sign_bundle(bundle, identity, entitlements):
    folders = (".framework", ".app", ".bundle", ".plugin", ".xpc", ".appex")
    contents = bundle / "Contents"
    entries = list(contents.rglob("*"))
    flags = ("--force", "--sign", identity, "--timestamp", "--options", "runtime")
    for path in entries:
        if is_macho(path):
            run("codesign", *flags, path)
    nested = sorted(
        (path for path in entries if path.is_dir() and not path.is_symlink() and path.suffix in folders),
        key=lambda path: len(path.parts),
        reverse=True,
    )
    for path in nested:
        run("codesign", *flags, path)
    run("codesign", *flags, "--entitlements", entitlements, bundle)
    run("codesign", "--verify", "--deep", "--strict", bundle)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("app", type=Path)
    parser.add_argument("output_zip", type=Path)
    parser.add_argument("--identity", required=True, help="Developer ID Application identity name or fingerprint")
    parser.add_argument("--entitlements", required=True, type=Path)
    parser.add_argument("--notary-profile", required=True, help="Existing notarytool Keychain profile")
    args = parser.parse_args()
    if not args.app.is_dir() or args.app.suffix != ".app":
        parser.error("app must be an existing .app bundle")
    if not args.entitlements.is_file():
        parser.error("entitlements must be an existing plist")
    if not args.output_zip.parent.is_dir() or args.output_zip.exists() or args.output_zip.suffix != ".zip":
        parser.error("output_zip must be a new .zip path in an existing directory")
    identity = signing_identity(args.identity)
    run("plutil", "-lint", args.entitlements)
    with tempfile.TemporaryDirectory(prefix="chiaki-notarize-", dir="/private/tmp") as directory:
        stage = Path(directory)
        bundle = stage / args.app.name
        run("ditto", "--norsrc", "--noextattr", "--noacl", args.app, bundle)
        sign_bundle(bundle, identity, args.entitlements)
        upload = stage / "upload.zip"
        run("ditto", "-c", "-k", "--norsrc", "--keepParent", bundle, upload)
        reply = json.loads(capture(
            "xcrun", "notarytool", "submit", upload, "--keychain-profile", args.notary_profile,
            "--wait", "--output-format", "json",
        ))
        if reply.get("status") != "Accepted":
            raise SystemExit(f"Notarization was not accepted. Submission ID: {reply.get('id', 'unavailable')}")
        run("xcrun", "stapler", "staple", bundle)
        run("xcrun", "stapler", "validate", bundle)
        run("spctl", "--assess", "--type", "execute", bundle)
        run("ditto", "-c", "-k", "--norsrc", "--keepParent", bundle, args.output_zip)


if __name__ == "__main__":
    main()
