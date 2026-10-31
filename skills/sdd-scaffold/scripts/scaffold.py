#!/usr/bin/env python3
"""Create the bundled SDD documentation, preserving every existing file."""

import argparse
import os
from pathlib import Path
import sys


ASSETS = Path(__file__).resolve().parent.parent / "assets" / "scaffold"


def safe_components(path, is_file=False):
    """Reject symlinks (including dangling ones) and non-directory parents."""
    parts = list(reversed(path.parents)) + [path]
    for part in parts:
        if part.is_symlink():
            raise ValueError(f"symbolic link: {part}")
        if part.exists() and (part != path or not is_file) and not part.is_dir():
            raise ValueError(f"not a directory: {part}")
    if is_file and path.exists() and not path.is_file():
        raise ValueError(f"not a regular file: {path}")


def plan(target):
    safe_components(target)
    actions = []
    for source in sorted(ASSETS.rglob("*")):
        if source.is_symlink():
            raise ValueError(f"symbolic link in assets: {source}")
        if not source.is_file():
            continue
        relative = source.relative_to(ASSETS)
        destination = target / relative
        safe_components(destination, is_file=True)
        if not destination.exists():
            status = "create"
        elif destination.read_bytes() == source.read_bytes():
            status = "unchanged"
        else:
            status = "conflict"
        actions.append((status, relative, source, destination))
    if not actions:
        raise ValueError("scaffold assets are missing or empty")
    return actions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    # Normalize '..' without resolving symbolic links away before checking them.
    raw_target = args.target.expanduser().absolute()
    try:
        safe_components(raw_target)
        target = Path(os.path.abspath(raw_target))
        actions = plan(target)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    for status, relative, _, _ in actions:
        print(f"{status}: {relative.as_posix()}")
    if any(status == "conflict" for status, *_ in actions):
        print("Conflicts found; no files written.", file=sys.stderr)
        return 2
    if args.dry_run:
        print("Dry run; no files written.")
        return 0
    created = 0
    try:
        for status, _, source, destination in actions:
            if status != "create":
                continue
            safe_components(destination, is_file=True)
            destination.parent.mkdir(parents=True, exist_ok=True)
            # Exclusive creation also prevents overwriting a concurrent new file.
            with destination.open("xb") as output:
                output.write(source.read_bytes())
            created += 1
    except (OSError, ValueError) as error:
        print(f"error after {created} creations: {error}; existing files preserved",
              file=sys.stderr)
        return 2
    print(f"Created {created}; unchanged {len(actions) - created}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
