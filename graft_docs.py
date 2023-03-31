"""
Script to aid gh-pages documentation updates.

Example usage:

- Create a venv and activate it
- Build documentation in the usual way (e.g., as in the test-doc-build workflow)
- Check out the gh-pages branch in a directory alongside this one; the worktree
  command is useful for this.
      git worktree add ../docs gh-pages-staging
- Graft newly-built docs onto that branch with
      python graft_docs.py
- Commit and push the changes.


"""

# XXX Don't hard-code ROOT_DIR, GH_PAGES_DIR, ...
# XXX Add argparse interface.
# XXX Remove .buildinfo


import pathlib
import re
import shutil


HERE = pathlib.Path(__file__)

ROOT_DIR = HERE.parent
GH_PAGES_DIR = ROOT_DIR.parent / "docs"
NEW_DOCS_DIR = ROOT_DIR / "docs" / "build" / "html"

#: Matcher for names of directories containing historical docs.
OLD_DOCS_MATCHER = re.compile(r"\d+\.\d+").fullmatch

# Remove everything that's not hidden and that doesn't match
# a directory for previous versions.

for child in GH_PAGES_DIR.iterdir():
    if child.name.startswith("."):
        # Ex: .git, .nojekyll
        print(f"Skipping {child.name}")
        continue
    if child.is_dir() and OLD_DOCS_MATCHER(child.name):
        print(f"Skipping {child.name}")
        continue
    print(f"Removing {child}")
    if child.is_file():
        child.unlink()
    elif child.is_dir():
        shutil.rmtree(child)

# Copy new docs into place.
for child in NEW_DOCS_DIR.iterdir():
    if child.is_file():

        shutil.copyfile(child, GH_PAGES_DIR / child.name)
    elif child.is_dir():
        shutil.copytree(child, GH_PAGES_DIR / child.name)
    print(child)

# List what's there.
