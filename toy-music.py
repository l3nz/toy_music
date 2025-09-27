import argparse
from pathlib import Path
from rename import Rename


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir",
                        help="display a square of a given number",
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
    print(f"- {cmd}")
    if (do_it):
        if cmd[0] == Rename.ACTION_RENAME:
            (_cmd, d, f, t) = cmd
            Path(f"{d}/{f}").rename(f"{d}/{t}")
        else:
            print("  ---- Unknown command!")


if __name__ == "__main__":
    main()
