# AGENTS.md — Envisage

Envisage is an extensible application framework for building plugin-based
Python applications, part of the Enthought Tool Suite (ETS). It uses the
Traits library for typed attributes and the Pyface/TraitsUI libraries for
UI components.

## Virtual Environment

Before installing or running anything, create and activate an isolated
virtual environment to avoid modifying the system Python:

```bash
uv venv --seed
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows
```

`uv` is the recommended tool. If it is not available, `python -m venv .venv`
works too.

## Build and Install

```bash
python -m pip install -e .
```

Dependencies: `traits>=6.2`, `apptools[preferences]>=5.3`, `pyface`,
`traitsui`.

## Running Tests

Tests use `unittest.TestCase` throughout. Both `pytest` and `unittest`
runners are supported. Install `pytest` first if using that runner:

```bash
python -m pip install pytest
```

```bash
# Run the full test suite with pytest
python -m pytest

# Run a single test file
python -m pytest envisage/tests/test_application.py

# Run a single test class
python -m pytest envisage/tests/test_service_registry.py::ServiceRegistryTestCase

# Run a single test method
python -m pytest envisage/tests/test_service_registry.py::ServiceRegistryTestCase::test_should_get_required_service

# Run with unittest directly
python -m unittest discover -v envisage

# Run a single test via unittest
python -m unittest envisage.tests.test_application.ApplicationTestCase.test_home
```

Some tests require a GUI toolkit (PySide6). On Linux, use `xvfb-run -a`
to run headless.

## Linting and Formatting

Style is enforced by Black, isort, and flake8. Install all required tools:

```bash
python -m pip install -r .github/workflows/style-requirements.txt
```

Run all three checks:

```bash
python -m black --check --diff .
python -m isort --check --diff .
python -m flake8 .
```

To auto-fix formatting:

```bash
python -m black .
python -m isort .
```

### Key style settings

- **Line length**: 79 (Black, isort, flake8 all configured to 79)
- **Black**: default settings with `line-length = 79`
- **isort**: `profile = "black"`, custom `ENTHOUGHT` import section
- **flake8**: ignores `E203`, `E266`, `W503`; `F401` suppressed in `*/api.py`

## Code Style Guidelines

### Copyright Header

Every `.py` file must start with the standard copyright header. Use whatever
end year is present in the existing files (currently 2026):

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

Imports are sorted by isort into six sections with labeled comment headers:

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

The sections are: `FUTURE`, `STDLIB`, `THIRDPARTY`, `ENTHOUGHT`
(apptools, pyface, traits, traitsui), `FIRSTPARTY` (envisage), `LOCALFOLDER`
(relative imports). Always import from `.api` submodules for Enthought
packages (e.g., `from traits.api import ...`, not `from traits.has_traits
import ...`). Use relative imports for intra-package references in library
code; use absolute imports (`from envisage.xxx`) in tests.

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

## Pull Requests

If a PR was created with agent assistance, the PR description must say so.
For example, add a note at the end such as:

> *This PR was created with the assistance of an AI coding agent.*
