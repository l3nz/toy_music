"""
The command make-playlists.py

Creates or updates the m3u playlist of a folder.
"""

import argparse
from pathlib import Path


def main():
    "Main entry point"
    parser = argparse.ArgumentParser(
        prog="make-playlists.py",
        description="""
Creates the m3u playlist of a folder, or recreates it if the mp3 files
in the folder have changed (files added or removed).

The playlist lists all the mp3 files in the folder and its sub-folders,
sorted first by sub-folder and then by file name. Paths in the playlist
are relative to the folder, so the drive can be mounted anywhere.
""",
        epilog="""
Usage:

  %(prog)s /Volumes/DRIVE/Album           # prints changes
  %(prog)s --run /Volumes/DRIVE/Album     # actually writes the playlist
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

    if not args.dir.is_dir():
        parser.error(f"{args.dir} is not a folder")

    changed = process_folder(args.dir.resolve(), args.run)

    if changed and not args.run:
        print("\n*** No changes made - to make changes, run with --run flag")


def is_visible(p: Path) -> bool:
    "Skips hidden files and macOS '._' metadata files"
    return not p.name.startswith(".")


def find_m3u(folder: Path):
    "Returns the existing m3u/m3u8 files directly in the folder"
    return sorted(f for f in folder.iterdir()
                  if f.is_file() and is_visible(f)
                  and f.suffix.lower() in (".m3u", ".m3u8"))


def mp3_files(folder: Path):
    """
    All the mp3 files in the folder and its sub-folders, as paths
    relative to the folder. Files directly in the folder come first,
    then each sub-folder in order; within a folder, by file name.
    """
    def sort_key(rel: Path):
        return ([p.lower() for p in rel.parent.parts], rel.name.lower())

    files = [f.relative_to(folder) for f in folder.rglob("*")
             if f.is_file() and f.suffix.lower() == ".mp3"
             and all(is_visible(Path(p)) for p in f.relative_to(folder).parts)]
    return sorted(files, key=sort_key)


def read_playlist(playlist: Path):
    "The entries of a playlist, ignoring comments and empty lines"
    text = playlist.read_text(encoding="utf-8", errors="replace")
    lines = (line.strip().replace("\\", "/") for line in text.splitlines())
    return [line for line in lines if line and not line.startswith("#")]


def process_folder(folder: Path, do_it: bool) -> bool:
    """
    Creates or recreates the playlist of the folder, if needed.
    Returns True if the playlist had to be written.
    """
    entries = [f.as_posix() for f in mp3_files(folder)]
    existing = find_m3u(folder)

    if existing:
        playlist = existing[0]
        old_entries = read_playlist(playlist)
        if old_entries == entries:
            print(f"- {folder.name}: {playlist.name} is up to date")
            return False
        added = sorted(set(entries) - set(old_entries))
        removed = sorted(set(old_entries) - set(entries))
        print(f"- {folder.name}: recreating {playlist.name} "
              f"({len(entries)} files, {len(added)} added, {len(removed)} removed)")
        for f in added:
            print(f"    + {f}")
        for f in removed:
            print(f"    - {f}")
        if not added and not removed:
            print("    (same files, different order)")
    else:
        if not entries:
            print(f"- {folder.name}: no mp3 files, nothing to do")
            return False
        playlist = folder / f"{folder.name}.m3u"
        print(f"- {folder.name}: creating {playlist.name} with {len(entries)} files")
        for f in entries:
            print(f"    {f}")

    if do_it:
        lines = ["#EXTM3U"] + entries
        playlist.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


if __name__ == "__main__":
    main()
