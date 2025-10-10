"""Create portfolio_minimal.zip excluding large/private artifacts.

Excludes:
- .venv/
- db.sqlite3
- removed_for_portfolio/
- portfolio_minimal.zip (if present)

Run from repository root with the project's Python.
"""
import os
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'portfolio_minimal.zip'
EXCLUDE = {'.venv', 'db.sqlite3', 'removed_for_portfolio', '.git', OUT.name}

def should_exclude(path: Path):
    # exclude if any path part matches EXCLUDE
    for part in path.parts:
        if part in EXCLUDE:
            return True
    return False

with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    for dirpath, dirnames, filenames in os.walk(ROOT):
        root = Path(dirpath)
        # skip excluded dirs early
        if should_exclude(root.relative_to(ROOT)):
            # prevent walk from descending
            dirnames[:] = []
            continue
        for f in filenames:
            fp = root / f
            rel = fp.relative_to(ROOT)
            if should_exclude(rel):
                continue
            # skip the zip itself
            if fp == OUT:
                continue
            z.write(fp, rel.as_posix())

print('Created', OUT)
