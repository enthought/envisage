# AGENTS.md — Envisage

Envisage is an extensible application framework for building plugin-based
Python applications, part of the Enthought Tool Suite (ETS). It uses the
Traits library for typed attributes and the Pyface/TraitsUI libraries for
UI components.

## Repository Layout

The `envisage` package lives in `src/envisage`, with tests in `tests`
subpackages alongside the code they exercise. `examples/legacy` holds an
unmaintained example that isn't part of the package; the maintained demos
are in `src/envisage/examples/demo`.

## Virtual Environment

The commands in this file all use `uv run`, which creates `.venv` on
demand and syncs it with Envisage in editable mode plus the `dev`
dependency group, which uv includes by default. There is no separate
install step.

Run `uv sync` if you want the environment created up front, for an editor
or language server to point at:

```bash
uv sync
```

## Dependencies

Runtime: `traits>=6.2`, `apptools[preferences]>=5.3`, `pyface`, `traitsui`.

Development requirements are dependency groups in `pyproject.toml`:
`test` (pytest), `gui` (PySide6), `style` (ruff) and `docs`. The default
`dev` group includes the first three, so it covers everything but `docs`.

Exact versions are pinned in the tracked `uv.lock`, which `uv run` and
`uv sync` install from. After changing anything in `pyproject.toml`, run
`uv lock` and commit the result — CI passes `--locked`, which fails on a
stale lockfile.

## Running Tests

```bash
uv run -m pytest
```

Some tests require a GUI toolkit (PySide6). Importing Pyface's toolkit
constructs a `QApplication`, so where no display is available those tests
abort the whole run rather than failing or skipping. Run headless with Qt's
offscreen platform plugin, as CI does on every platform:

```bash
QT_QPA_PLATFORM=offscreen uv run -m pytest
```

## Linting and Formatting

Style is enforced by ruff, provided by the `dev` group. Run both checks:

```bash
uv run -m ruff check .
uv run -m ruff format --check --diff .
```

To auto-fix:

```bash
uv run -m ruff check --fix .
uv run -m ruff format .
```

### Key style settings

- **Line length**: 88, ruff's default
- **Lint rules**: `CPY001` (copyright header), `E`, `F`, `I`, `W`;
  `F401` suppressed in `*/api.py`
- **Import sorting**: ruff's `I` rules, with a custom `enthought` section
- **ruff version**: upper-bounded to `~= 0.16.0`, because ruff changes
  formatting in minor releases. Raising the bound means reformatting the
  codebase in the same change.

## Code Style Guidelines

### Copyright Header

Every non-empty `.py` file must start with the standard copyright header,
enforced by ruff's `CPY001` rule. The authoritative text, including the year
range, is the `notice-rgx` setting in `pyproject.toml`; that copy is a regular
expression, so unescape it rather than pasting it verbatim:

```python
# (C) Copyright 2007-2026 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
```

### Import Ordering

Imports are sorted by ruff into six sections with labeled comment headers:

```python
# Standard library imports.
import logging
import os

# Enthought library imports.
from traits.api import HasTraits, Instance, List, Str

# Local imports.
from .extension_point import ExtensionPoint
from .i_application import IApplication
```

The sections are: `future`, `standard-library`, `third-party`, `enthought`
(apptools, pyface, traits, traitsui), `first-party` (envisage) and
`local-folder` (relative imports). Always import from `.api` submodules for
Enthought packages (e.g., `from traits.api import ...`, not `from
traits.has_traits import ...`). Use relative imports for intra-package
references in library code; use absolute imports (`from envisage.xxx`) in
tests.

### Type System

This project does **not** use PEP 484 type annotations. All typing is done
through the Traits type system (`Str`, `Int`, `Instance(...)`, `List`,
`Dict`, `Bool`, `Event`, etc.). Do not add type annotations to function
signatures or variables.

### Naming Conventions

- **Classes**: `PascalCase` — `Application`, `PluginManager`, `ServiceRegistry`
- **Interfaces**: `I`-prefix — `IApplication`, `IPlugin`, `IServiceRegistry`
- **Functions/methods**: `snake_case` — `get_extensions`, `register_service`
- **Private methods/traits**: single underscore — `_create_event`, `_services`
- **Constants**: `UPPER_SNAKE_CASE` — `SERVICE_OFFERS`, `PREFERENCES`
- **Module logger**: always `logger = logging.getLogger(__name__)`

### Docstrings

- Modules/classes/methods: imperative mood, concise (`"""Run the application."""`)
- Trait initializers: `"""Trait initializer."""`
- Trait property getters: `"""Trait property getter."""`
- Trait change handlers: `"""Static trait change handler."""`
- Functions and methods should use PEP 257 and the NumPy docstring standard,
  including `Parameters` and `Returns` sections where appropriate
- Class attributes (especially Traits) are documented with `#:` comments
  above the declaration, not in docstrings

### Trait Documentation

Document traits with `#:` comments above the declaration:

```python
#: The application's globally unique identifier.
id = Str
```

### Error Handling

- Custom exceptions inherit from `Exception` directly
- Use `logger.exception(...)` when catching and re-raising
- The `# fixme:` comment tag (lowercase) is used for known issues;
  always include a reference to a GitHub issue

### String Formatting

Use `%`-style formatting for logger calls (lazy evaluation):
`logger.debug("service <%d> registered %s", service_id, name)`. For other
strings, `.format()` and f-strings are both acceptable.

### Testing Conventions

- Framework: `unittest.TestCase` (not bare pytest functions)
- Test classes: `<Name>TestCase` (e.g., `ApplicationTestCase`)
- Test methods: `test_<descriptive_name>` in snake_case
- Assertions: `self.assertEqual`, `self.assertTrue`, `self.assertIs`, etc.
- Use `self.assertRaises` as context manager: `with self.assertRaises(ValueError):`
- Define helper classes (interfaces, plugins) inside test methods as needed
- Prefer `self.addCleanup(...)` for teardown where practical; `tearDown` methods are also acceptable when clearer

## Changelog

Add an entry to `CHANGES.rst` under the in-development section at the top,
grouped under a heading such as `Fixes`, `Tests` or `Build`. End it with the
number of the **pull request**, not the issue it closes — `(#635)`, or
`(#618, #621)` for a change spread over several PRs.

## Pull Requests

If a PR was created with agent assistance, the PR description must say so.
For example, add a note at the end such as:

> *This PR was created with the assistance of an AI coding agent.*
