#!/usr/bin/env python3
"""Set launch settings and the minimum macOS required by the bundled binaries."""

from pathlib import Path
import plistlib
import re
import subprocess
import sys

bundle = Path(sys.argv[1])
plist = bundle / "Contents/Info.plist"
metadata = plistlib.loads(plist.read_bytes())
versions = [metadata.get("LSMinimumSystemVersion", "0")]
magic_numbers = {
    bytes.fromhex(value)
    for value in ("feedface", "cefaedfe", "feedfacf", "cffaedfe", "cafebabe", "bebafeca", "cafebabf", "bfbafeca")
}
for path in (bundle / "Contents").rglob("*"):
    if path.is_symlink() or not path.is_file():
        continue
    with path.open("rb") as handle:
        is_macho = handle.read(4) in magic_numbers
    if not is_macho:
        continue
    result = subprocess.run(["xcrun", "vtool", "-arch", "arm64", "-show-build", path],
                            capture_output=True, text=True)
    minimums = re.findall(r"(?m)^\s*minos\s+([\d.]+)", result.stdout)
    if not minimums:
        minimums = re.findall(r"(?m)^\s*version\s+([\d.]+)", result.stdout)
    versions.extend(minimums)
metadata["LSMinimumSystemVersion"] = max(versions, key=lambda value: tuple(map(int, value.split("."))))
metadata["CFBundleName"] = "Chiaki-ng Metal"
metadata["CFBundleDisplayName"] = "Chiaki-ng Metal"
metadata.setdefault("LSEnvironment", {})["CHIAKI_VIDEOTOOLBOX_METAL"] = "1"
plist.write_bytes(plistlib.dumps(metadata))
print("Declared minimum macOS", metadata["LSMinimumSystemVersion"])
