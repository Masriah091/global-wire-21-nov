# main.py - hand-in for THE GLOBAL WIRE, challenger R5 (NI21, @maseiah990).
# The artwork is finished and committed next to this file as entry.png.
# At run time there is nothing left to draw: this script only delivers a
# copy of entry.png into the folder the runner points at through the
# MAKEFUN_OUTPUT_DIR environment variable (falling back to /output when
# the variable is unset or empty). No path is hardcoded as the only
# destination, and nothing outside this folder is read.

import os
import shutil
from pathlib import Path


def deliver() -> Path:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)

    source = Path(__file__).resolve().parent / "entry.png"
    target = out_dir / source.name
    shutil.copyfile(source, target)
    return target


if __name__ == "__main__":
    placed = deliver()
    print(f"delivered {placed} ({placed.stat().st_size} bytes)")
