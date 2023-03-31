"""
Helper script for gh-pages documentation updates.

Example usage
-------------
Assuming that the gh-pages branch has been checked out into ../docs
(for example using `git worktree add ../docs gh-pages`), and that
documentation has been built locally via Sphinx and is in docs/build/html:

After an update to the main branch, to update the docs in the root directory
of the gh-pages branch, do:

    python graft_docs.py docs/build/html ../docs

After releasing version 7.3.2 (for example) of the package, to update the
docs in the 7.3/ subdirectory of the gh-pages branch, do:

    python graft_docs.py docs/build/html ../docs --tag 7.3.2
"""

import argparse
import pathlib
import re
import shutil

#: Matcher for names of directories containing release docs.
RELEASE_DOCS_DIR_MATCHER = re.compile(r"\d+\.\d+").fullmatch


def subdir_from_tagname(version: str) -> str:
    """
    Map a version tag (e.g., '7.2.1') to the gh-pages subdirectory containing
    docs for that tag (e.g., '7.2').
    """
    subdir = ".".join(version.split(".")[:2])
    if not RELEASE_DOCS_DIR_MATCHER(subdir):
        raise RuntimeError(
            f"tagname {version} does not have the expected form"
        )
    return subdir


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
            if RELEASE_DOCS_DIR_MATCHER(child.name):
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


def main() -> None:
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
    parser.add_argument(
        "--tag",
        help="Release tag name (when updating for a release)",
    )
    args = parser.parse_args()

    if args.tag is None:
        target = args.target
    else:
        target = args.target / subdir_from_tagname(args.tag)
        if not target.exists():
            print(f"Creating target directory {target}")
            target.mkdir()

    remove_existing_docs(target)
    copy_new_docs(args.source, target)


if __name__ == "__main__":
    main()
