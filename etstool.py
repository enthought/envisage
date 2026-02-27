# (C) Copyright 2007-2026 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""
Tasks for Test Runs
===================

This file is intended to be used with a python environment with the
click library to automate the process of setting up test environments
and running the test within them.  This improves repeatability and
reliability of tests be removing many of the variables around the
developer's particular Python environment.  Test environment setup and
package management is performed using `EDM
<http://docs.enthought.com/edm/>`_

To use this to run your tests, you will need to install EDM and click
into your working environment.  You will also need to have git
installed to access required source code from github repositories.
You can then do::

    python etstool.py install --runtime=... --toolkit=...

to create a test environment from the current codebase and::

    python etstool.py test --runtime=... --toolkit=...

to run tests in that environment.  You can remove the environment with::

    python etstool.py cleanup --runtime=... --toolkit=...

If you make changes you will either need to remove and re-install the
environment or manually update the environment using ``edm``, as
the install performs a ``pip install`` rather than a ``pip install -e``,
so changes in your code will not be automatically mirrored in the test
environment.  You can update with a command like::

    edm run --environment ... -- pip install .

You can run all three tasks at once with::

    python etstool.py test_clean --runtime=... --toolkit=...

which will create, install, run tests, and then clean-up the environment.  And
you can run tests in all supported runtimes and toolkits (with cleanup)
using::

    python etstool.py test_all

For currently-supported runtime values, see the 'available_runtimes' value. For
toolkits, see 'available_toolkits'. Not all combinations of toolkits and
runtimes will work; the 'supported_combinations' variable describes which
combinations are supported.

Tests can still be run via the usual means in other environments if that suits
a developer's purpose.

Changing This File
------------------

To change the packages installed during a test run, change the dependencies
variable below.

Other changes to commands should be a straightforward change to the listed
commands for each task. See the EDM documentation for more information about
how to run commands within an EDM enviornment.

"""

import glob
import os
import subprocess
import sys
from contextlib import contextmanager
from shutil import copy as copyfile
from shutil import rmtree, which
from tempfile import mkdtemp

import click

# Python runtime versions supported by this tool.
available_runtimes = ["3.8", "3.11"]

# Python runtime used by default.
default_runtime = "3.8"

# Toolkits supported by this tool.
# PySide2 and PyQt5 are not (currently) available for EDM + Python 3.8, so we
# don't support them here.
available_toolkits = ["null", "pyqt6", "pyside6"]

# Toolkit used by default.
default_toolkit = "null"

supported_combinations = {
    "3.8": {"null", "pyqt6", "pyside6"},
    "3.11": {"null", "pyqt6", "pyside6"},
}

dependencies = {
    "apptools",
    "configobj",
    "coverage",
    "enthought_sphinx_theme",
    "pyface",
    "sphinx",
    "sphinx_copybutton",
    "traits",
    "traitsui",
}

# Dependencies we install from PyPI
pypi_dependencies = {
    # style packages; install from PyPI to make sure that we're compatible
    # with the style checks used in the check-style.yml workflow
    "black~=23.0",
    "flake8",
    "flake8-ets",
    "isort",
}

# Dependencies we install from source for cron tests
# Order from packages with the most dependencies to one with the least
# dependencies. Packages are forced re-installed in this order.
source_dependencies = [
    "apptools",
    "traitsui",
    "pyface",
    "traits",
]

# Toolkit dependencies installed from EDM.
toolkit_dependencies = {
    "pyside6": {"pyside6"},
    "pyqt6": {"pyqt6"},
}

runtime_dependencies = {}

github_url_fmt = "git+http://github.com/enthought/{0}.git#egg={0}"

# Options shared between different click commands.
edm_option = click.option(
    "--edm",
    help=(
        "Path to the EDM executable to use. The default is to use the first "
        "EDM found in the path. The EDM executable can also be specified "
        "by setting the ETSTOOL_EDM environment variable."
    ),
    envvar="ETSTOOL_EDM",
)
runtime_option = click.option(
    "--runtime",
    default=default_runtime,
    type=click.Choice(available_runtimes),
    show_default=True,
    help="Python runtime version",
)
toolkit_option = click.option(
    "--toolkit",
    default=default_toolkit,
    type=click.Choice(available_toolkits),
    show_default=True,
    help="GUI toolkit",
)
environment_option = click.option(
    "--environment",
    default=None,
    help=(
        "EDM environment name to use in place of the "
        "automatically constructed name"
    ),
)
source_option = click.option(
    "--source/--no-source",
    default=False,
    help="Install ETS packages from source",
)
editable_option = click.option(
    "--editable/--not-editable",
    default=False,
    help="Install main package in 'editable' mode?  [default: --not-editable]",
)


@click.group()
def cli():
    pass


# Subgroup for checking and fixing style


@cli.group()
def style():
    """
    Commands for checking style and applying style fixes.
    """


@cli.command()
@edm_option
@runtime_option
@toolkit_option
@environment_option
@editable_option
@source_option
def install(edm, runtime, toolkit, environment, editable, source):
    """Install project and dependencies into a clean EDM environment."""
    parameters = get_parameters(edm, runtime, toolkit, environment)
    packages = " ".join(
        dependencies
        | toolkit_dependencies.get(toolkit, set())
        | runtime_dependencies.get(runtime, set())
    )
    # edm commands to setup the development environment
    commands = [
        "{edm} environments create {environment} --force --version={runtime}",
        "{edm} --config edm.yaml install -y -e {environment} " + packages,
    ]
    commands.extend(
        [
            "{edm} run -e {environment} -- pip install " + dep
            for dep in pypi_dependencies
        ]
    )

    click.echo("Creating environment '{environment}'".format(**parameters))
    execute(commands, parameters)

    if source:
        # Remove EDM ETS packages and install them from source
        cmd_fmt = (
            "{edm} plumbing remove-package "
            "--environment {environment} --force "
        )
        commands = [cmd_fmt + source_pkg for source_pkg in source_dependencies]
        execute(commands, parameters)
        source_pkgs = [
            github_url_fmt.format(pkg) for pkg in source_dependencies
        ]
        # Without the --no-dependencies flag such that new dependencies on
        # main branch are brought in.
        commands = [
            "python -m pip install --force-reinstall {pkg}".format(pkg=pkg)
            for pkg in source_pkgs
        ]
        commands = [
            "{edm} run -e {environment} -- " + command for command in commands
        ]
        execute(commands, parameters)

    # Always install local source at the end to mitigate risk of testing
    # against a distributed release.
    if editable:
        install_cmd = (
            "{edm} run -e {environment} -- "
            "python -m pip install --editable . --no-dependencies"
        )
    else:
        install_cmd = (
            "{edm} run -e {environment} -- "
            "python -m pip install . --no-dependencies"
        )
    execute([install_cmd], parameters)

    click.echo("Done install")


@cli.command()
@edm_option
@runtime_option
@toolkit_option
@environment_option
def shell(edm, runtime, toolkit, environment):
    """Create a shell into the EDM development environment
    (aka 'activate' it).

    """
    parameters = get_parameters(edm, runtime, toolkit, environment)
    commands = [
        "{edm} shell -e {environment}",
    ]
    execute(commands, parameters)


@style.command(name="check")
@edm_option
@runtime_option
@toolkit_option
@environment_option
def style_check(edm, runtime, toolkit, environment):
    """
    Run style checks.
    """
    parameters = get_parameters(edm, runtime, toolkit, environment)
    commands = [
        "{edm} run -e {environment} -- python -m black --check --diff .",
        "{edm} run -e {environment} -- python -m isort --check --diff .",
        "{edm} run -e {environment} -- python -m flake8 .",
    ]
    execute(commands, parameters)


@style.command(name="fix")
@edm_option
@runtime_option
@toolkit_option
@environment_option
def style_fix(edm, runtime, toolkit, environment):
    """
    Run style fixers.

    This automatically fixes any black or isort failures, but it won't
    automatically fix all flake8 errors.
    """
    parameters = get_parameters(edm, runtime, toolkit, environment)
    commands = [
        "{edm} run -e {environment} -- python -m black .",
        "{edm} run -e {environment} -- python -m isort .",
    ]
    execute(commands, parameters)


@cli.command()
@edm_option
@runtime_option
@toolkit_option
@environment_option
def test(edm, runtime, toolkit, environment):
    """Run the test suite in a given environment with the specified toolkit."""
    parameters = get_parameters(edm, runtime, toolkit, environment)
    environ = dict(PYTHONUNBUFFERED="1")
    commands = [
        (
            "{edm} run -e {environment} -- python -W default -m "
            "coverage run -p -m unittest discover -v envisage"
        ),
    ]

    # We run in a tempdir to avoid accidentally picking up wrong envisage
    # code from a local dir.  We need to ensure a good .coveragerc is in
    # that directory, plus coverage has a bug that means a non-local coverage
    # file doesn't get populated correctly.
    click.echo("Running tests in '{environment}'".format(**parameters))
    with do_in_tempdir(files=[".coveragerc"], capture_files=["./.coverage*"]):
        os.environ.update(environ)
        execute(commands, parameters)
    click.echo("Done test")


@cli.command()
@edm_option
@runtime_option
@toolkit_option
@environment_option
def cleanup(edm, runtime, toolkit, environment):
    """Remove a development environment."""
    parameters = get_parameters(edm, runtime, toolkit, environment)
    commands = [
        "{edm} environments remove {environment} --purge -y",
    ]
    click.echo("Cleaning up environment '{environment}'".format(**parameters))
    execute(commands, parameters)
    click.echo("Done cleanup")


@cli.command()
@edm_option
@runtime_option
@toolkit_option
def test_clean(edm, runtime, toolkit):
    """Run tests in a clean environment, cleaning up afterwards"""
    args = ["--toolkit={}".format(toolkit), "--runtime={}".format(runtime)]
    if edm is not None:
        args.append("--edm={}".format(edm))

    try:
        install(args=args, standalone_mode=False)
        test(args=args, standalone_mode=False)
    finally:
        cleanup(args=args, standalone_mode=False)


@cli.command()
@edm_option
@runtime_option
@toolkit_option
@environment_option
@editable_option
def update(edm, runtime, toolkit, environment, editable):
    """Update/Reinstall package into environment."""
    parameters = get_parameters(edm, runtime, toolkit, environment)
    if editable:
        install_cmd = (
            "{edm} run -e {environment} -- "
            "python -m pip install --editable . --no-dependencies"
        )
    else:
        install_cmd = (
            "{edm} run -e {environment} -- "
            "python -m pip install . --no-dependencies"
        )
    commands = [install_cmd]
    click.echo("Re-installing in  '{environment}'".format(**parameters))
    execute(commands, parameters)
    click.echo("Done update")


@cli.command()
@edm_option
def test_all(edm):
    """Run test_clean across all supported environment combinations."""
    failed_command = False
    for runtime, toolkits in supported_combinations.items():
        for toolkit in toolkits:
            args = [
                "--toolkit={}".format(toolkit),
                "--runtime={}".format(runtime),
            ]
            if edm is not None:
                args.append("--edm={}".format(edm))

            try:
                test_clean(args, standalone_mode=True)
            except SystemExit:
                failed_command = True
    if failed_command:
        sys.exit(1)


@cli.command()
@edm_option
@runtime_option
@toolkit_option
@environment_option
def docs(edm, runtime, toolkit, environment):
    """Build HTML documentation."""

    parameters = get_parameters(edm, runtime, toolkit, environment)
    parameters["docs_source"] = "docs/source"
    parameters["docs_build"] = "docs/build"
    parameters["docs_source_api"] = docs_source_api = "docs/source/api"
    parameters["templates_dir"] = "docs/source/api/templates/"

    # Remove any previously autogenerated API documentation.
    doc_api_files = os.listdir(docs_source_api)
    permanent = ["envisage.api.rst", "templates"]
    previously_autogenerated = [
        file for file in doc_api_files if file not in permanent
    ]
    for file in previously_autogenerated:
        os.remove(os.path.join(docs_source_api, file))

    html_build_command = (
        "{edm} run -e {environment} -- python -m sphinx -b html "
        "{docs_source} {docs_build}"
    )

    commands = [html_build_command]
    execute(commands, parameters)


# Utility routines


def get_parameters(edm, runtime, toolkit, environment):
    """Set up parameters dictionary for format() substitution"""

    if edm is None:
        edm = locate_edm()

    if environment is None:
        environment = "envisage-test-{runtime}-{toolkit}".format(
            runtime=runtime, toolkit=toolkit
        )

    parameters = {
        "edm": edm,
        "runtime": runtime,
        "toolkit": toolkit,
        "environment": environment,
    }

    if toolkit not in supported_combinations[runtime]:
        msg = (
            "Runtime {runtime} and toolkit {toolkit} not supported by "
            + "test environments"
        )
        raise click.ClickException(msg.format(**parameters))
    return parameters


@contextmanager
def do_in_tempdir(files=(), capture_files=()):
    """Create a temporary directory, cleaning up after done.

    Creates the temporary directory, and changes into it.  On exit returns to
    original directory and removes temporary dir.

    Parameters
    ----------
    files : sequence of filenames
        Files to be copied across to temporary directory.
    capture_files : sequence of filenames
        Files to be copied back from temporary directory.
    """
    path = mkdtemp()
    old_path = os.getcwd()

    # send across any files we need
    for filepath in files:
        click.echo("copying file to tempdir: {}".format(filepath))
        copyfile(filepath, path)

    os.chdir(path)
    try:
        yield path
        # retrieve any result files we want
        for pattern in capture_files:
            for filepath in glob.iglob(pattern):
                click.echo("copying file back: {}".format(filepath))
                copyfile(filepath, old_path)
    finally:
        os.chdir(old_path)
        rmtree(path)


def execute(commands, parameters):
    for command in commands:
        click.echo("[EXECUTING] {}".format(command.format(**parameters)))
        try:
            subprocess.check_call(
                [arg.format(**parameters) for arg in command.split()]
            )
        except subprocess.CalledProcessError as exc:
            click.echo(str(exc))
            sys.exit(1)


def locate_edm():
    """
    Locate an EDM executable if it exists, else raise an exception.

    Returns the first EDM executable found on the path. On Windows, if that
    executable turns out to be the "edm.bat" batch file, replaces it with the
    executable that it wraps: the batch file adds another level of command-line
    mangling that interferes with things like specifying version restrictions.

    Returns
    -------
    edm : str
        Path to the EDM executable to use.

    Raises
    ------
    click.ClickException
        If no EDM executable is found in the path.
    """
    edm = which("edm")
    if edm is None:
        raise click.ClickException(
            "This script requires EDM, but no EDM executable "
            "was found on the path."
        )

    # Resolve edm.bat on Windows.
    if sys.platform == "win32" and os.path.basename(edm) == "edm.bat":
        edm = os.path.join(os.path.dirname(edm), "embedded", "edm.exe")

    return edm


if __name__ == "__main__":
    cli()
