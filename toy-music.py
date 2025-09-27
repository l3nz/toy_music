"""
The command toy-music.py
"""

import argparse
from pathlib import Path
from rename import Rename


def main():
    "Main entry point"
    parser = argparse.ArgumentParser(
        prog="toy-music.py",
        description="""
Rewrites a set of mp3s to be played in sequence on Toyota audio players.

To do this, it prefixes each file with an incremental code, e.g.
myfile.mp3 becomes  0001-myfile.mp3

Files that are already prefixed won't be changed; and new files
will be prefixed after them.

""",
        epilog="""
Usage:

  %(prog)s /Volumes/DRIVE           # prints changes
  %(prog)s --run /Volumes/DRIVE     # actually applies changes
    """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("dir",
                        help="The folder to process",
                        type=Path)
    parser.add_argument("--run",
                        help="Actually makes changes",
                        action="store_true")
    args = parser.parse_args()

    r = Rename()
    r.files_of(args.dir)
    r.keep_good_files()
    print(f"From {args.dir} - {r.stats()}\n")
    changes = r.process_files()

    for c in changes:
        apply_change(c, args.run)

    if (not args.run):
        print("\n*** No changes made - to make changes, run with --run flag")


def apply_change(cmd, do_it):
    "This executes cmmands created by Rename"
    print(f"- {cmd}")
    if (do_it):
        if cmd[0] == Rename.ACTION_RENAME:
            (_cmd, d, f, t) = cmd
            Path(f"{d}/{f}").rename(f"{d}/{t}")
        else:
            print("  ---- Unknown command!")


if __name__ == "__main__":
    main()
