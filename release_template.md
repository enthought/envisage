---
name: Tracking issue
about: Use this template for upcoming releases.
title: "[Release Number] Release Checklist"
---

Target date:

Release Candidate by DD/MM/YYYY

Release by DD/MM/YYYY

Release candidate
-------------------
- [ ] Verify that all relevant PRs have been merged to master.
- [ ] Create a PR against master to bump version number, merge that PR
- [ ] From the commit just before bumping the version, create a new branch `maint/<release version number>`
- [ ] Make sure `maint/<release version number>` is included (somehow) in the following block in appveyor.yml 
```
branches:
  only:
    - ...
```
- [ ] Update changelog and open PR targeting a new `maint/<release version number>` branch
- [ ] Update `ci-src-requirements.txt` if needed
- [ ] Check MANIFEST and requirements are still up to date.
- [ ] Update version in setup.py for the prerelease, open a PR against maint/<release version number>
       - Create a new branch from maint/<release version number>: `git checkout maint/<release version number>; git pull; git checkout -b call-it-anything-you-like`
       - Set PRERELEASE to "rc1" and IS_RELEASED to true, commit, e.g.git commit -m "Set IS_RELEASED to true for prerelease <release version number>rc1"
       - Flip IS_RELEASED back to false, commit.
       - Open a PR against maint/<release version number>
       - Merge but DO NOT SQUASH
No squashing so that the tagged commit in the next step will be on the branch (Kit: It is not a big deal even if it was squashed. But some prefer having the commit on the branch.) Alternatively, flip the IS_RELEASED flag in a separate PR.
- [ ] Tag (annotated!) the release candidate on the commit where IS_RELEASED is set to true, e.g. git tag -a -m "Release candidate <release version number>rc1" <release version number>rc1 <commit-hash>
- [ ] Push the tag to GitHub
- [ ] Upload to PyPI
       - `git checkout <tag>`, `git clean -ffxd`, `python setup.py sdist`, `twine check dist/<...>.tar.gz`, `twine upload dist/<...>.tar.gz`
- [ ] Announcement for the release candidate

Release blockers
----------------
- [ ]

Pre-release
---
- [ ] Backport PRs that have been merged to master to the maintenance branch. Use the "need backport ..." tag if there is one (but don't rely 100% on it)
- [ ] Verify that no other open issue needs to be addressed before the release.
- [ ] Test against other ETS packages and other traitsui-using projects
- [ ] Check MANIFEST, requirements, changelog are still up to date.
- [ ] Test building the documentation

Release
-------
- [ ] Create branch release/<release version number> from maint/<release version number> branch.
        - Set release to <release version number>, and set IS_RELEASED is true; commit
        - Open a PR against maint/<release version number> with this being the last commit so that CI is built on the release commit
        - Bump the micro version number i.e. <release version number + 0.0.1> and set IS_RELEASED to false; commit, don't push yet.
        - Once CI is done building the last commit, push the commit
        - Merge but do not squash so that the release commit is on the branch (Kit: Again, not a big deal even if it was squashed.)
- [ ] Restore the release/<release version number> branch (Kit: not sure why we are keeping them, but we are it seems)
- [ ] From the commit at which IS_RELEASED is true and version is <release version number>, tag (annotated!) `git tag -a -m "Release <release version number>" <release version number>`
- [ ] Push the tag `git push origin <release version number>`
- [ ] Make PR targeting `gh-pages` branch: Generate documentation and copy the content to the branch. Verify that the resulting index.html looks good.
- [ ] Install from source distribution and run tests again (Kit: perhaps this should be moved up to go before merging the release PR?)
- [ ] Upload to PyPI
- [ ] Test the PyPI package

Post-release
-------------
- [ ] Package update for `enthought/free` repository (for EDM)
- [ ] Backport release note and change log to master, and possibly `maint/<release version number>` branch.
- [ ] Update GitHub Release pages https://github.com/enthought/traitsui/releases
- [ ] Announcement (e.g. Google Group)
