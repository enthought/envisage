=================
 Release history
=================

Version 7.0.0
=============

Released: 2023-03-24

This is a major release aimed at modernization and cleanup of some out-of-date
code. In particular, this release removes the IPython-related plugins, and
drops support for Python 3.6.

Thanks to:

* Mark Dickinson
* Chengyu Liu
* Corran Webster

Features
--------
* There's a new ``unbind_extension_point`` function that reverses the effects
  of ``bind_extension_point``. This can be useful for clean teardown. (#546)
* All id string constants that were previously available from ``envisage.ids``
  are now also exported in ``envisage.api``. Users are encouraged to import
  everything they need from ``envisage.api``, and to open an issue if anything
  they need is not exported in ``envisage.api``. (#508)

Changes
-------
* When exiting a ``TasksApplication``, the plugins are now stopped after
  exiting the event loop. Previously they were stopped while the event loop was
  still running, causing some lifecycle issues. (#524)
* The ``extension_registry`` argument to ``bind_extension_point`` is no
  longer optional, and ``ExtensionPointBinding`` will no longer look for
  an extension registry on the ``ExtensionPoint`` class. (#545)
* Operations that used to raise ``SystemError`` now raise something more
  appropriate. In particular, the ``PluginManager.start_plugin`` and
  ``PluginManager.stop_plugin`` methods now raise ``ValueError`` rather
  than ``SystemError`` when given an invalid plugin id. (#529)
* ``envisage.__version__`` is no longer defined. If you need the Envisage
  version at runtime, use ``importlib.metadata`` to retrieve it. (#513)
* Python 3.6 is no longer supported. All current versions of Python (3.7
  through 3.11) are supported. (#513)

Fixes
-----
* The ``repr`` of a ``Plugin`` instance now correctly uses the name of the
  plugin class. (#535)

Deprecations
------------
* The ``EggPluginManager``, ``EggBasketPluginManager`` and
  ``PackagePluginManager`` are deprecated, and will be removed in Envisage 8.0.
  (#540)
* The ``include`` and ``exclude`` traits on the ``PluginManager`` are
  deprecated, and will be removed in Envisage 8.0. (#544)

Removals
--------
* Plugins and machinery related to IPython have been removed. Specifically,
  the ``IPythonKernelPlugin`` and ``IPythonKernelUIPlugin`` plugins have been
  removed, along with supporting classes ``InternalIPKernel`` and
  ``IPKernelApp``. (#496)
* The ``ExtensionPoint.bind`` method has been removed. (#545)
* The previously deprecated ``safeweakref.ref`` class has been removed. (#522)
* Some legacy unmaintained examples have been removed. (#557)

Documentation
-------------
* The changelog is now included in the built documentation. (#550)

Tests
-----
* Old-style namespace packages used for testing have been replaced with
  normal non-namespace packages. This fixes some warnings from the latest
  ``setuptools``. (#543)
* The test suite now runs cleanly under ``pytest``. (#539)
* Tests that are skipped due to a PySide6 problem should now be run
  if the version of PySide6 is recent enough. (#554)

Build
-----
* Package configuration now uses ``pyproject.toml`` in place of the old
  ``setup.py``-based configuration. (#513)
* Optional dependencies are no longer declared. (#513)
* A new style-checking workflow has been added that runs ``black``, ``isort``
  and ``flake8`` over the codebase, and new code is expected to comply with
  ``black`` and ``isort`` configurations. (#549)
* A new documentation-build workflow has been added. The built documentation
  is uploaded as an artifact. (#551)

Version 6.1.1
=============

Released: 2023-02-07

This is a bugfix release that fixes an incompatibility between the workbench
code and the latest Traits version, among other minor fixes.

Thanks to:

* Mark Dickinson
* Prabhu Ramachandran
* Scott Talbert

Fixes
-----
* A trait validation error in the Workbench ``DefaultActionSet`` has been
  fixed. This fixes a compatibility issue with Traits 6.4. (#485)
* Initialization of application directories now correctly respects the
  value of ``self.state_location``. (#490)
* In the test suite, egg generation now uses ``sys.executable`` to ensure
  it picks up the correct Python executable. (#499)

Other changes
-------------
* The version of PySide6 used in test workflows has been restricted. (#487)
* The EDM version used in test workflow has been updated. (#484)
* Various fixes have been made to the GitHub Actions workflows, for
  compatibility with the newest runners. (#491, #494)
* Copyright headers have been updated for 2023. (#493)


Version 6.1.0
=============

Released: 2022-08-15

This is a minor feature release whose main focus is on compatibility with
Python 3.8 and PySide 6. It includes a collection of other cleanups and minor
fixes.

In this release, there are some changes in the way that the Envisage
``Application`` interacts with ``ETSConfig``. You should double check that
the locations of user data, preferences and application home directories are
the ones that you expect after upgrading.

Please note that the IPython-related portions of Envisage are currently not
compatible with the latest versions of ipykernel and IPython available from
PyPI. This has been made explicit in this release in the form of version
restrictions on those packages in the ``envisage[ipython]`` install target.

Thanks to:

* Aaron Ayres
* Mark Dickinson
* Sai Rahul Poruri
* Corran Webster

Changes
-------
* The ``Application.user_data`` directory no longer includes the id
  of the application, but instead matches the ``ETSConfig.user_data``. (#467)
* The Envisage ``Application`` will no longer try to change the
  ``ETSConfig.application_home`` attribute. (#467)
* The ``PackageResourceProtocol`` now uses ``importlib.resources`` instead
  of ``pkg_resources``. (#466)
* The IPython-related features of Envisage require ipykernel version < 6 and
  IPython version < 8. (#449)

Fixes
-----
* Fix EggPluginManager to use current pkg_resources.working_set. (#444)

Refactoring and maintenance
---------------------------
* Simplify ImportManager by using importlib. (#465)
* Update end year in copyright headers. (#458)

Tests
-----
* The tests no longer rely on pre-built eggs for test packages. (#459, #436)
* Skip tests for recent ipykernel, and add check for IPython version. (#457)
* Work around a Python 3.6 issue with ``isinstance`` and lru caches in tests.
  (#470)
* Fix an ``EggBasketPluginManager`` test that only passed due to test
  interactions. (#443)
* Some pickles used in testing have been regenerated in order to work
  correctly with more recent versions of Traits. (#472)
* Fix poorly specified action and menu groups in tests. (#468)
* Fix test hangs with PySide2 / macOS 11. (#454)
* Skip an ipykernel-using test if ipykernel is not available in the test
  environment. (#423)

Examples
--------
* Fixes for the Attractors example. (#408, #416)

Documentation
--------------
* Code samples in the documentation now have a "copy" button. (#474)
* Stylistic changes and updates to documentation. (#406)
* Fix documentation links to examples on main branch. (#447)
* Add a Read the Docs config file. (#434)
* Miscellaneous minor fixes. (#435)

Build and CI
------------
* Update build machinery to support Python 3.8 and PySide 6. (#477)
* Add workflow to automatically upload releases to PyPI. (#478)
* Set up Slack notification for cron jobs. (#433)
* Cron job failures are now reported to the main Slack channel, not
  to the bots channel. (#473)
* Add GitHub Actions workflow to test PyPI install. (#450)
* The default branch has been renamed from master to main. (#446)
* Update classifiers for Python 3.10. (#437)
* Port CI from Appveyor to GitHub Actions. (#432, #426)
* Simplify flake8 command in ``etstool.py``. (#431)
* Traits version 6.2 or later is now required. (#410)


Version 6.0.1
=============

Released: 2021-06-18

This bugfix release fixes the issue where Extension Point resolution was
happening too eagerly, which caused issues during application startup time in
certain cases. We recommend all users of Envisage to upgrade to this bugfix
version.

Fixes
-----

- Revert PR #354, which caused the issue #417. (#422)

Tests
-----

- Ensure that the testsuite passes with minimal dependencies. (#423)
- Add a regression test for issue #417. (#421)

Version 6.0.0
=============

Released: 2021-05-14

This major release focuses on speeding up Envisage applications. We achieved
this speedup by removing unused functionality in the package. Specifically,
we removed the ``@contributes_to`` decorator and the code needed to handle
methods decorated with the above decorator.

Additionally, with this release, parts of envisage start using the new traits
observation framework instead of the old traits ``on_trait_change``. So,
Envisage now depends on Traits version >= 6.2.

Features
--------
- Support ``observe(name:items)`` for Extension Points. (#354)

Changes
-------
- Replace ``Either`` trait type with ``Union``. (#405)
- Rewrite ``*_changed`` static trait handlers to use ``observe``. (#401)
- Replace ``depends_on`` in ``Property`` traits with ``observe``. (#400)
- Change default pickle protocol to be compatible with Python >= 3.4. (#390)

Removals
--------
- Remove ``contributes_to`` decorator and supporting code. (#402)
- Remove unnecessary return statements throughout the codebase. (#393)

Build
-----
- Ensure that the cron job installs all necessary dependencies. (#383)


Version 5.0.0
=============

Released: 2020-12-03

This is a major release mainly relating to code modernization. In this
release, support for Python versions <3.6 have been dropped. The
class_load_hooks and single_project modules have been removed. Additionally,
there were various fixes to bugs, examples, tests, and documentation. Demo
examples are also distributed as package data such that they are visible via
the "etsdemo" GUI application (to be installed separately).

Features
--------

- Re-export CorePlugin in envisage.api (#332)
- Create and fill plugin subpackage api modules (#323)
- Add relevant classes to envisage.ui.tasks.api (#322)

Fixes
-----

- Fix index slice in ExtensionPointChangedEvent when plugin changes (#357)
- Fix ValueError from unregistering services when application stops (#345)
- Fix the MOTD example (#319)
- Fix the Hello_World example (#318)
- Fix the attractors tasks application example (#317)
- Make TasksApplication.gui expect an IGUI interface, not a GUI instance (#301)

Documentation
-------------

- Contribute examples to etsdemo (#380)
- Refactor documentation links to source on GitHub (#379)
- Make example run from any directory (#377)
- Setup intersphinx in docs (#343)
- Add documentation for envisage APIs (#340)
- Use jinja templates for API documentation (#339)
- Improve API docs : document traits (#334)
- Rebuild documentation, mostly to fix search functionality (#290)

Deprecations
------------

- Deprecate safeweakref and replace its uses (#275)

Removals
--------

- Drop support for Python 3 versions older than Python 3.6. (#341)
- Remove single_project (#331)
- Remove class_load_hooks and ClassLoadHook (#321)

Tests
-----

- Add tests for ExtensionRegistry getters (#349)
- Add tests to demonstrate behaviour when mutating extension point directly
  (#346)
- Use mixin instead of having ProviderExtensionRegistryTestCase inherit from
  ExtensionRegistryTestCase (#335)
- Switch on default warning flag for CI test command (#326)
- Add test eggs for Python 3.9 and remove eggs for Python 2.7 (#289)

Build
-----

- Turn off macOS builds on Travis CI (#375)
- Fix CI cron job setup to install apptools (#348)
- Update setup.py to allow prerelease version (#344)
- Add wx as being supported in etstool, add it back to CI, and test against
  wxPython v4.x (#336)
- Update EDM version to 3.0.1 in Travis CI and Appveyor. (#297)
- Stop reporting code coverage in CI (#288)
- Fix CI setup on Linux, Windows (#287)
- Remove support for PySide and PyQt4 from CI (#285)
- Add Slack notification for Travis CI runs (#283)
- Add flake8 check to etstool and CI (#268)


Version 4.9.2
=============

Released: 2020-02-17

This is a bugfix release that fixes tests that assumed the existence
of categories machinery (which is removed in Traits 6.0.0).

Fixes
-----

- Conditionally skip tests that fail against Traits 6.0.0 due to the removal
  of Categories. (#263)


Version 4.9.1
=============

Released: 2020-02-13

This is a bugfix release aimed at ensuring compatibility with the
upcoming Traits 6.0.0 release.

Fixes
-----

- Fix tests that fail against Traits 6.0.0 due to the removal
  of double nesting in list events. (#255)
- Replace a comment mention of ``AdaptedTo`` with ``Supports``. (#253)
- Remove dependence on ``clean_filename`` from Traits. (#252)
- Replace a use of the deprecated ``DictStrAny`` trait with
  ``Dict(Str, Any)``. (#250)


Version 4.9.0
=============

Released: 2019-11-19

This is a minor feature release with a small handful of fixes, and a single
new feature to make the ``IPythonKernelPlugin`` easier to use for applications.

Features
--------

- Add an option to allow the ``InternalIPKernel`` to initialise its kernel at
  kernel creation time. At some point in the future, this will become the
  default behaviour. (#227)

Fixes
-----

- Replace a use of the deprecated ``adapts`` function with
  ``register_factory``. (#234)
- In the ``IPKernelApp``, correctly restore the original state of
  ``IPython.utils.io.std*`` streams even if those streams didn't exist
  originally. (#232)
- Remove duplicate copyright header from autogenerated version file. (#220)

Tests
-----

- Remove a ``print`` call from a unit test. (#240)
- Add unit tests for the ``envisage.ui.single_project`` adapters. (#235)
- Add unit tests to check that ``InternalIPKernel`` doesn't affect
  ``sys.path``. (#233)
- Fix the test suite not to write to the user's ``~/.ipython`` directory.
  (#231)
- Fix the test suite not to write to the user's ``~/.enthought`` directory.
  (#230)
- Remove an unused import and a useless ``tearDown`` method in the
  ``IPythonKernel`` tests. (#223)
- Fix ``DeprecationWarning``s from uses of long-deprecated ``TestCase``
  methods. (#222)
- Add test eggs for Python 3.8. (#214)

Build
-----

- Rename changelog extension from ``.txt`` to ``.rst``. (#238)
- Update EDM version used in Travis CI and Appveyor. (#236)
- Add ``mock`` to test dependencies on Python 2. (#229)
- Fix status badges in ``README``. (#216)


Version 4.8.0
=============

Released: 2019-09-13

The main focus of this feature release is the ``IPythonKernelPlugin``, which
has been updated to work with the latest IPython-related packages from PyPI,
and is now much more careful about releasing resources allocated.

Also in this release, a number of outdated, incomplete or otherwise
nonfunctional pieces of code were removed.

Features
--------

- Improved ``repr`` for ``ExtensionPoint`` objects. (#142)

Changes
-------

- Drop support for Python versions older than 2.7 and Python 3 versions older
  than Python 3.5. (#139)
- The ``IPythonKernelPlugin`` now releases all allocated resources (threads,
  file descriptors, etc.) and undoes global state changes at plugin ``stop``
  time. (#188)
- Suppress the Ctrl-C message printed by the IPython kernel at start time.
  (#182)
- Add license headers to all files, and make license header statements
  consistent. (#192)

Fixes
-----

- Use a fixed pickle protocol when saving task layout state, to avoid
  cross-Python-version difficulties. (#179)
- Fix deprecation warnings from use of ``Logger.warn``. (#178)
- Fix some Python 3 syntax errors in example scripts. (#171)

Removals
--------

- Remove the unsupported and incomplete ``UpdateCheckerPlugin``. (#199)
- Remove the ``plugin.debug`` empty submodule. (#195)
- Remove the old ``IPythonShell`` plugin, which was based on pre-IPython 1.0.
  (#173)
- Remove the non-functional ``RefreshCodePlugin``. (#202)
- Remove ``project_runnable``, which was never functional. (#169)
- Remove outdated debugging fallback from the ``ExtensionPoint`` source. (#167)
- Remove ``FBIPlugin``. (#166)
- Remove the ``remote_editor`` plugins. (#137)

Documentation
-------------

- Add docstrings for tasks plugin extension points. (#181)
- Fix incorrect documentation for ``always_use_default_layout``. (#177)
- Spell "Pyface" correctly. (#176)
- NumPyDoc style fixes. (#168)
- Add API documentation, with corresponding build infrastructure. (#165)
- Fix invalid syntax in Tetris example. (#158)
- Use the Enthought Sphinx Theme for documentation. (#157)

Tests
-----

- Remove dependency on the ``nose`` package, and rename test modules. All
  tests can now be discovered and run using ``unittest``. (#200, #194)

Build
-----

- Revise version-handling mechanisms and other minor details
  in ``setup.py`` script. (#197, #190)
- Remove unused and outdated ``tox.ini`` file. (#201)
- Update ``etstool.py`` to work with a non-EDM bootstrap environment on
  Windows. (#203)
- Test against other ETS packages from source, using Travis CI cron jobs.
  (#162)
- Fix deprecated pieces in Travis CI configuration. (#160, #159)
- Update EDM version used, and clean up and simplify Travis CI and
  Appveyor configurations. (#152)
- Usability improvements to ``etstool.py``. (#145, #148)


Version 4.7.2
=============

Released: 03 May 2019

Fixes
-----

* Fix some broken imports and name errors in the ``envisage.developer``
  package. (#130)
* Add missing test data to support running tests on Python 3.7. (#136)
* Fix reversed interpretation of the
  ``TasksApplication.always_use_default_layout`` when creating task windows.
  (#144)
* In the ``InternalIPKernel`` plugin, restore original standard streams
  (``stdout``, ``stdin``, ``stderr``) at plugin stop time. (#146)
* In the ``InternalIPKernel`` plugin, fix ``ResourceWarnings`` from
  unclosed pipes attached to qt consoles. (#147)


Version 4.7.1
=============

Released : 31 January 2019

Changes
-------

* Replace use of deprecated ``HasTraits.set`` method (#118)

Fixes
-----

* Fix IPython GUI kernel issue when used with ipykernel 4.7.0 (#123)
* Fix infinite recursion issue when harvesting extension methods (#121)


Version 4.7.0
=============

Changes
-------

* Update CI setup and include ``ipykernel`` in devenv (#105, #111, #114)
* Use ``--gui`` rather than ``--matplotlib`` when starting IPython kernel (#101)
* Downgrade level of a logging message (#95)

Fixes
-----

* Fix old-style relative import (#109)
* Fix attractors example (#103)
* Stop the IOPubThread as part of IPython kernel shutdown (#100)
* Fix Sphinx conf to be able to build docs again (#91)
* Fix deprecated IPython import (#92)
* Fix task layout serialization under Python 3 (#90)


Version 4.6.0
=============

This is an incremental release, mainly consisting of bug fixes.  The most
significant change is the support for IPython >= 4 in the IPython plugin.

Thanks to @corranwebster, @dpinte, @itziakos, @jonathanrocher, @kamalx,
@rahulporuri, @robmcmullen, @sjagoe

Enhancements
------------

* IPython kernel plugin now supports IPython >= 4 (#82)
* Remove usage of deprecated IPython QtConsole API (#80)
* Defer selection of toolkit and avoid creating GUI applications as side-effects as
  much as possible (#77, #76)

Fixes
-----

* Fixes for tests under Python 3.5 (#86)
* Work around for issue with Traits in Python 3 (#78)
* Replace uses of ‘file’ and ‘execfile’ (#75)
* Fix MOTD_Using_Eggs example (#66)
* Fix broken and outdated links in documentation (#72)
* Fix link to docs from README (#70)
* Fix degenerate case where window is created with no layout (#44)


Version 4.5.1
=============

Enhancements
------------

* Add tox for testing package install (#67)

Fixes
-----

* Include missing test files in the package data (#67)
* Include missing test cases for Python 3.4 (#67)


Version 4.5.0
=============

New features
------------

* IPythonKernelPlugin for Tasks: run an IPython kernel within the
  envisage app and expose it as a service (#54).
* Envisage now supports Python 3.4 (#61).

Enhancements
------------

* Allow loading plugins from an egg basket even when some eggs are
  invalid (#40, #46).
* Add a simple ``GUIApplication`` to bootstrap basic plugin-driven
  applications (#34).
* Split the IPython kernel and IPython menu action into two separate
  plugins for flexibility (#57).

Fixes
-----

* Use new Traits interfaces and adaptation implementation (#37).
* Envisage now configures the logger with a ``NullHandler`` to avoid
  spurios unconfigured logger warnings (#45).
* Envisage no longer swallows exceptions in plugin startup (#50).
* Various fixes to continuous integration configuration (#47, #60).


Version 4.4.0
=============

The major component of this feature is to work with the new
``traits.adaptation`` mechanism in place of the deprecated
``traits.protocols``, maintaining compatibility with ``traits`` version
4.4.0.

This release also adds a new method to retrieve a service that is
required by the application and provides documentation and test updates.


New features
------------

* Added a simple GUIApplication class (673c8f6)
* Added a method to get a required service (94dfdea)

Enhancements
------------

* Updated to use the new traits.adaptation functionality (34fa5e6)

Fixes
-----

* Updated links to point to github instead of svn codebase (87cdb87)
* Fixed test cases and added to Travis-CI (6c11d9f)
