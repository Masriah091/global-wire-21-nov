# main.py - hand-in program for Variant E "THE GLOBAL WIRE".
# Copies the pre-rendered entry.png from this directory into the
# MAKEFUN_OUTPUT_DIR (default /output) as entry.png.
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst)


if __name__ == "__main__":
    main()
