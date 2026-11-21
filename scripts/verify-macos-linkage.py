#!/usr/bin/env python3
"""Normalize Mach-O install IDs and check that the app can run without Homebrew."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("app", type=Path)
parser.add_argument("--relocate", action="store_true")
options = parser.parse_args()
contents = options.app / "Contents"
frameworks = contents / "Frameworks"
magic = {bytes.fromhex(x) for x in ("cffaedfe", "feedfacf", "cafebabe", "cafebabf")}


def is_macho(path):
    if path.is_symlink() or not path.is_file():
        return False
    with path.open("rb") as handle:
        return handle.read(4) in magic


def command(*args):
    return subprocess.check_output(args, stderr=subprocess.DEVNULL, text=True)


def allowed(path):
    return path.startswith(("@rpath/", "@loader_path/", "@executable_path/", "/usr/lib/", "/System/"))


def verify(path):
    name = path.relative_to(contents)
    object_id = command("otool", "-D", path).splitlines()[1:]
    load_commands = command("otool", "-l", path)
    rpaths = set(re.findall(r"cmd LC_RPATH\s+cmdsize \d+\s+path (.+?) \(offset", load_commands))
    build_rpaths = {value for value in rpaths if value.startswith("/") and not allowed(value)}
    changes = []
    if object_id and not allowed(object_id[0]) and options.relocate:
        if path.is_relative_to(frameworks):
            changes.extend(("-id", "@rpath/" + path.relative_to(frameworks).as_posix()))
        else:
            changes.extend(("-id", "@loader_path/" + path.name))
    if build_rpaths and options.relocate:
        for value in sorted(build_rpaths):
            changes.extend(("-delete_rpath", value))
    if changes:
        command("install_name_tool", *changes, path)
    link_lines = command("otool", "-L", path).splitlines()[1:]
    references = [line.strip().split(" (compatibility")[0] for line in link_lines if line[:1].isspace()]
    if any(not allowed(reference) for reference in references) or (build_rpaths and not options.relocate):
        raise ValueError(f"Non-system dependency or absolute search path: {name}")


objects = [path for path in contents.rglob("*") if is_macho(path)]
if not objects:
    raise SystemExit("No Mach-O binaries found")
with ThreadPoolExecutor(max_workers=6) as threads:
    list(threads.map(verify, objects))
print(f"Checked linkage for {len(objects)} Mach-O binaries")
