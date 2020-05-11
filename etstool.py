#
#  Copyright (c) 2017, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in enthought/LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
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
the install performs a ``python setup.py install`` rather than a ``develop``,
so changes in your code will not be automatically mirrored in the test
environment.  You can update with a command like::

    edm run --environment ... -- python setup.py install

You can run all three tasks at once with::

    python etstool.py test_clean --runtime=... --toolkit=...

which will create, install, run tests, and then clean-up the environment.  And
you can run tests in all supported runtimes and toolkits (with cleanup)
using::

    python etstool.py test_all

The only currently supported runtime value is ``3.6``, and
currently supported toolkits are ``pyside``, ``pyside2``, ``pyqt``, ``pyqt5``,
``wx`` and ``null``. Not all combinations of toolkits and runtimes will work,
but the tasks will fail with a clear error if that is the case.

Tests can still be run via the usual means in other environments if that suits
a developer's purpose.

Changing This File
------------------

To change the packages installed during a test run, change the dependencies
variable below.  To install a package from github, or one which is not yet
available via EDM, add it to the `ci-src-requirements.txt` file (these will be
installed by `pip`).

Other changes to commands should be a straightforward change to the listed
commands for each task. See the EDM documentation for more information about
how to run commands within an EDM enviornment.

"""

import glob
import os
import subprocess
import sys
from shutil import rmtree, copy as copyfile, which
from tempfile import mkdtemp
from contextlib import contextmanager

import click

# Python runtime versions supported by this tool.
available_runtimes = ["3.6"]

# Python runtime used by default.
default_runtime = "3.6"

# Toolkits supported by this tool.
available_toolkits = ["pyside", "pyside2", "pyqt", "pyqt5", "wx", "null"]

# Toolkit used by default.
default_toolkit = "null"

supported_combinations = {
    "3.6": {"pyside2", "pyqt", "pyqt5", "null"},
}

dependencies = {
    "apptools",
    "coverage",
    "enthought_sphinx_theme",
    "flake8",
    "ipykernel",
    "pyface",
    "sphinx",
    "traits",
    "traitsui",
}

# Dependencies we install from source for cron tests
source_dependencies = {
    "pyface",
    "traits",
    "traitsui",
}

toolkit_dependencies = {
    "pyside": {"pyside"},
    # XXX once pyside2 is available in EDM, we will want it here
    "pyside2": set(),
    "pyqt": {"pyqt<4.12"},  # FIXME: build of 4.12-1 appears to be bad
    # XXX once pyqt5 is available in EDM, we will want it here
    "pyqt5": set(),
    # FIXME: wxpython 3.0.2.0-6 is broken of OS-X
    "wx": {"wxpython<3.0.2.0-6"},
    "null": set(),
}

runtime_dependencies = {}

environment_vars = {
    "pyside": {"ETS_TOOLKIT": "qt4", "QT_API": "pyside"},
    "pyside2": {"ETS_TOOLKIT": "qt4", "QT_API": "pyside2"},
    "pyqt": {"ETS_TOOLKIT": "qt4", "QT_API": "pyqt"},
    "pyqt5": {"ETS_TOOLKIT": "qt4", "QT_API": "pyqt5"},
    "wx": {"ETS_TOOLKIT": "wx"},
    "null": {"ETS_TOOLKIT": "null"},
}

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


@cli.command()
@edm_option
@runtime_option
@toolkit_option
@environment_option
@editable_option
@source_option
def install(edm, runtime, toolkit, environment, editable, source):
    """ Install project and dependencies into a clean EDM environment.

    """
    parameters = get_parameters(edm, runtime, toolkit, environment)
    packages = " ".join(
        dependencies
        | toolkit_dependencies.get(toolkit, set())
        | runtime_dependencies.get(runtime, set())
    )
    # edm commands to setup the development environment
    commands = [
        "{edm} environments create {environment} --force --version={runtime}",
        "{edm} install -y -e {environment} " + packages,
        (
            "{edm} run -e {environment} -- "
            "pip install -r ci-src-requirements.txt --no-dependencies"
        ),
    ]
    # pip install pyqt5 and pyside2, because we don't have them in EDM yet
    if toolkit == "pyqt5":
        commands.append(
            "{edm} run -e {environment} -- pip install pyqt5==5.9.2"
        )
    elif toolkit == "pyside2":
        commands.append(
            "{edm} run -e {environment} -- pip install pyside2==5.11"
        )

    if editable:
        install_cmd = (
            "{edm} run -e {environment} -- pip "
            "install --editable . --no-dependencies"
        )
    else:
        install_cmd = (
            "{edm} run -e {environment} -- pip install . --no-dependencies"
        )
    commands.append(install_cmd)

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
        commands = [
            "python -m pip install {pkg} --no-deps".format(pkg=pkg)
            for pkg in source_pkgs
        ]
        commands = [
            "{edm} run -e {environment} -- " + command for command in commands
        ]
        execute(commands, parameters)
    click.echo("Done install")


@cli.command()
@edm_option
@runtime_option
@toolkit_option
@environment_option
def flake8(edm, runtime, toolkit, environment):
    """ Run a flake8 check in a given environment.

    """
    parameters = get_parameters(edm, runtime, toolkit, environment)
    commands = ["{edm} run -e {environment} -- python -m flake8"]
    execute(commands, parameters)


@cli.command()
@edm_option
@runtime_option
@toolkit_option
@environment_option
def test(edm, runtime, toolkit, environment):
    """ Run the test suite in a given environment with the specified toolkit.

    """
    parameters = get_parameters(edm, runtime, toolkit, environment)
    environ = environment_vars.get(toolkit, {}).copy()
    environ["PYTHONUNBUFFERED"] = "1"
    commands = [
        (
            "{edm} run -e {environment} -- "
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
    """ Remove a development environment.

    """
    parameters = get_parameters(edm, runtime, toolkit, environment)
    commands = [
        "{edm} run -e {environment} -- python setup.py clean",
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
    """ Run tests in a clean environment, cleaning up afterwards

    """
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
    """ Update/Reinstall package into environment.

    """
    parameters = get_parameters(edm, runtime, toolkit, environment)
    if editable:
        install_cmd = (
            "{edm} run -e {environment} -- "
            "pip install --editable . --no-dependencies"
        )
    else:
        install_cmd = (
            "{edm} run -e {environment} -- pip install . --no-dependencies"
        )
    commands = [install_cmd]
    click.echo("Re-installing in  '{environment}'".format(**parameters))
    execute(commands, parameters)
    click.echo("Done update")


@cli.command()
@edm_option
def test_all(edm):
    """ Run test_clean across all supported environment combinations.

    """
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
    """ Build HTML documentation. """

    parameters = get_parameters(edm, runtime, toolkit, environment)
    parameters["docs_source"] = "docs/source"
    parameters["docs_build"] = "docs/build"
    parameters["docs_source_api"] = docs_source_api = "docs/source/api"

    # Remove any previously autogenerated API documentation.
    if os.path.exists(docs_source_api):
        rmtree(docs_source_api)

    apidoc_command = (
        "{edm} run -e {environment} -- python -m sphinx.ext.apidoc "
        "-o {docs_source_api} envisage */tests"
    )
    html_build_command = (
        "{edm} run -e {environment} -- python -m sphinx -b html "
        "{docs_source} {docs_build}"
    )

    commands = [apidoc_command, html_build_command]
    execute(commands, parameters)


# Utility routines

def get_parameters(edm, runtime, toolkit, environment):
    """ Set up parameters dictionary for format() substitution """

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
            "Python {runtime} and toolkit {toolkit} not supported by "
            + "test environments"
        )
        raise RuntimeError(msg.format(**parameters))
    return parameters


@contextmanager
def do_in_tempdir(files=(), capture_files=()):
    """ Create a temporary directory, cleaning up after done.

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
