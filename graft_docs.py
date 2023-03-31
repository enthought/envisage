"""
Helper script for gh-pages documentation updates.

This script assumes that you already have the gh-pages branch checked out
locally and that the documentation has been built and is available in
another local directory (e.g., docs/build/html).
"""

import argparse
import pathlib
import re
import shutil

#: Matcher for names of directories containing historical docs.
OLD_DOCS_MATCHER = re.compile(r"\d+\.\d+").fullmatch


def remove_existing_docs(docs_dir: pathlib.Path) -> None:
    """
    Remove existing documentation files and directories.

    Skips hidden files and directories (like .nojekyll and .git), and
    ignores directories whose name matches <major>.<minor> - these are
    directories that contain previous documentation versions.
    """
    print(f"Removing existing documentation from {docs_dir} ...")
    for child in docs_dir.iterdir():
        if child.name.startswith("."):
            print(f"  Not removing hidden file or directory {child}")
        elif child.is_file():
            print(f"  Removing file {child}")
            child.unlink()
        elif child.is_dir():
            if OLD_DOCS_MATCHER(child.name):
                print(f"  Not removing old docs directory {child}")
            else:
                print(f"  Removing directory {child}")
                shutil.rmtree(child)
        else:
            raise RuntimeError("Not a file or directory: {child}: aborting")


def copy_new_docs(source_docs: pathlib.Path, target_dir: pathlib.Path) -> None:
    """
    Copy new documentation into place.

    Copies newly-built docs from their build location (e.g., docs/build/html)
    to the target directory in the gh-pages branch.

    Hidden files and directories (for example .buildinfo, .nojekyll, .doctrees)
    are ignored.
    """
    print(f"Copying docs from {source_docs} to {target_dir} ...")
    for child in source_docs.iterdir():
        if child.name.startswith("."):
            print(f"  Not copying hidden file or directory {child.name}")
        elif child.is_file():
            print(f"  Copying file {child} to {target_dir}")
            shutil.copyfile(child, target_dir / child.name)
        elif child.is_dir():
            print(f"  Copying directory {child} to {target_dir}")
            shutil.copytree(child, target_dir / child.name)
        else:
            raise RuntimeError("Not a file or directory: {child}: aborting")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source",
        help="Directory containing newly-built documentation",
        type=pathlib.Path,
    )
    parser.add_argument(
        "target",
        help="Directory containing the gh-pages checkout",
        type=pathlib.Path,
    )
    args = parser.parse_args()
    remove_existing_docs(args.target)
    copy_new_docs(args.source, args.target)


if __name__ == "__main__":
    main()
