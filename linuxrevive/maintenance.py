from __future__ import annotations

import os
from pathlib import Path


def temporary_locations() -> tuple[Path, ...]:
    locations = [Path("/tmp")]
    user_cache = Path.home() / ".cache"
    if user_cache.is_dir():
        locations.append(user_cache)
    return tuple(locations)


def scan_temporary_files() -> tuple[int, int]:
    files = 0
    total = 0
    for location in temporary_locations():
        try:
            for entry in location.rglob("*"):
                if entry.is_file() and not entry.is_symlink():
                    files += 1
                    try:
                        total += entry.stat().st_size
                    except OSError:
                        continue
        except OSError:
            continue
    return files, total


def clear_user_cache() -> int:
    cache = Path.home() / ".cache"
    removed = 0
    if not cache.is_dir():
        return removed
    for entry in cache.iterdir():
        if entry.name == "keep":
            continue
        try:
            if entry.is_dir() and not entry.is_symlink():
                for child in sorted(entry.rglob("*"), reverse=True):
                    if child.is_file() or child.is_symlink():
                        child.unlink(missing_ok=True)
                    elif child.is_dir():
                        child.rmdir()
                entry.rmdir()
            elif entry.is_file() or entry.is_symlink():
                entry.unlink()
            removed += 1
        except OSError:
            continue
    return removed
