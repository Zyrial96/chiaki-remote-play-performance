#!/usr/bin/env python3
"""Export the staged source and pinned submodules, without Git metadata."""

import argparse
import io
from pathlib import Path
import subprocess
import tarfile


def git(repository, *args):
    return subprocess.check_output(["git", "-C", repository, *args])


def add_tree(output, repository, tree, prefix):
    with tarfile.open(fileobj=io.BytesIO(git(repository, "archive", tree))) as source:
        for item in source:
            if Path(item.name).name == "debug.keystore":
                continue
            item.name = f"{prefix}/{item.name}"
            output.addfile(item, source.extractfile(item) if item.isfile() else None)
    entries = git(repository, "ls-tree", "-rz", tree).split(b"\0")
    for entry in filter(None, entries):
        metadata, _, raw_path = entry.partition(b"\t")
        mode, _, object_id = metadata.decode("ascii").split()
        if mode == "160000":
            path = raw_path.decode("utf-8")
            submodule = repository / path
            if not (submodule / ".git").exists():
                raise SystemExit(f"Submodule is not initialized: {path}")
            if git(submodule, "rev-parse", "HEAD").strip() != object_id.encode():
                raise SystemExit(f"Submodule doesn't match pinned revision: {path}")
            add_tree(output, submodule, object_id, f"{prefix}/{path}")


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("source", type=Path)
parser.add_argument("output", type=Path)
args = parser.parse_args()
repository = args.source.resolve()
if args.output.exists():
    raise SystemExit("Output already exists")
temporary = args.output.with_name(args.output.name + ".part")
root = args.output.name.removesuffix(".tar.gz")
try:
    with tarfile.open(temporary, "w:gz", compresslevel=5) as archive:
        add_tree(archive, repository, git(repository, "write-tree").decode().strip(), root)
    temporary.rename(args.output)
finally:
    temporary.unlink(missing_ok=True)
