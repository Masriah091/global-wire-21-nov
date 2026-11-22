"""Hand-in entry point for THE GLOBAL WIRE (variant E).

The finished artwork ships in this folder as entry.png; at grading
time this script only has to place a copy of it where the runner
expects results, which is the folder named by MAKEFUN_OUTPUT_DIR
(falling back to /output).
"""

from pathlib import Path
import os


def deliver() -> Path:
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    target_dir.mkdir(parents=True, exist_ok=True)

    artwork = Path(__file__).resolve().parent / "entry.png"
    destination = target_dir / artwork.name
    destination.write_bytes(artwork.read_bytes())
    return destination


if __name__ == "__main__":
    placed = deliver()
    print(f"entry delivered: {placed} ({placed.stat().st_size} bytes)")
