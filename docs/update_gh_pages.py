# (C) Copyright 2007-2024 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""
Helper script for gh-pages documentation updates.

This script helps maintain the documentation in the gh-pages branch
of the repository; that documentation is automatically served by
GitHub and made available via docs.enthought.com.

The intended structure of the gh-pages branch is:

- the root directory contains documentation matching the contents
  of the 'main' branch of the codebase.
- named subdirectories with names of the form <major>.<minor> contain
  documentation for released versions of the package.
- the root directory also contains a 'latest' symlink pointing to the
  docs matching the latest release (i.e., the release with highest
  version number).

Example usage
-------------
In the examples below we assume that:

- the current working directory is the root of the repository
- the gh-pages branch has been checked out into ../docs
  (for example using `git worktree add ../docs gh-pages`)
- documentation has been built locally via Sphinx and is in docs/build/html

Then to update the docs in the root directory of the gh-pages branch (for
example after a push to the main branch), do:

    python docs/update_gh_pages.py docs/build/html ../docs

After releasing version 7.3.2 (for example) of the package, to update the
docs in the 7.3/ subdirectory of the gh-pages branch, do:

    python docs/update_gh_pages.py docs/build/html ../docs --tag 7.3.2

Note that for a bugfix release, the intention is that the docs for the bugfix
release (e.g., 7.3.2) overwrite the docs for the previous release with the same
<major>.<minor> version (e.g., 7.3.1). The docs end up in the 7.3/ subdirectory
of the gh-pages tree in both cases.
"""

import argparse
import pathlib
import re
import shutil

#: Matcher for names of directories containing release docs.
RELEASE_DOCS_DIR_MATCHER = re.compile(r"\d+\.\d+").fullmatch

#: Name of the symlink that points to the latest docs
LATEST = "latest"


def release_version(dir_name: str) -> list[int]:
    """
    Mapping from release docs directory names to orderable values.

    E.g., '7.13' -> (7, 13).
    """
    return [int(piece) for piece in dir_name.split(".")]


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


def update_latest_symlink(docs_dir: pathlib.Path) -> None:
    """
    Update the 'latest' symlink to point to documentation for the most recent
    release.

    docs_dir should point to the root gh-pages directory.
    """
    all_release_docs = [
        child.name
        for child in docs_dir.iterdir()
        if child.is_dir() and RELEASE_DOCS_DIR_MATCHER(child.name)
    ]
    latest_docs = max(all_release_docs, key=release_version)

    # Remove existing symlink if present.
    latest_symlink = docs_dir / LATEST
    if latest_symlink.is_symlink():
        print(f"Removing symlink {latest_symlink}")
        latest_symlink.unlink()

    # Create new symlink
    print(f"Updating symlink {latest_symlink} to point to {latest_docs}")
    latest_symlink.symlink_to(latest_docs, target_is_directory=True)


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
                print(f"  Not removing release docs directory {child}")
            elif child.is_symlink() and child.name == LATEST:
                print(f"  Not removing symlink {child}")
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
    if args.tag is not None:
        update_latest_symlink(args.target)


if __name__ == "__main__":
    main()
