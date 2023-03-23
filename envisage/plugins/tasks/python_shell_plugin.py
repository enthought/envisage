# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
"""
Module defining a simple Python shell Envisage tasks plugin.

This plugin provides a task with a simple Python shell.  This shouldn't be
confused with a more full-featured shell, such as those provided by IPython.
"""

# Standard library imports.
import logging

from pyface.tasks.contrib.python_shell import PythonShellTask

# Enthought library imports.
from traits.api import Dict, Instance, List, Property, Str

from envisage.api import ExtensionPoint, IExtensionRegistry, Plugin
from envisage.ui.tasks.api import TaskFactory

logger = logging.getLogger()

BINDINGS = "envisage.plugins.python_shell.bindings"
COMMANDS = "envisage.plugins.python_shell.commands"


class EnvisagePythonShellTask(PythonShellTask):
    """Subclass of PythonShellTask that gets its bindings and commands from
    an Envisage ExtensionPoint
    """

    id = "envisage.plugins.tasks.python_shell_task"

    # ExtensionPointUser interface
    extension_registry = Property(Instance(IExtensionRegistry))

    # The list of bindings for the shell
    bindings = ExtensionPoint(id=BINDINGS)

    # The list of commands to run on shell startup
    commands = ExtensionPoint(id=COMMANDS)

    # property getter/setters

    def _get_extension_registry(self):
        if self.window is not None:
            return self.window.application
        return None


class PythonShellPlugin(Plugin):
    """A tasks plugin to display a simple Python shell to the user."""

    # Extension point IDs.
    BINDINGS = BINDINGS
    COMMANDS = COMMANDS
    TASKS = "envisage.ui.tasks.tasks"

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = "envisage.plugins.tasks.python_shell_plugin"

    # The plugin's name (suitable for displaying to the user).
    name = "Python Shell"

    #### Extension points exposed by this plugin ##############################

    bindings = ExtensionPoint(
        List(Dict),
        id=BINDINGS,
        desc="""
        This extension point allows you to contribute name/value pairs that
        will be bound when the interactive Python shell is started.

        e.g. Each item in the list is a dictionary of name/value pairs::

            {'x' : 10, 'y' : ['a', 'b', 'c']}
        """,
    )

    commands = ExtensionPoint(
        List(Str),
        id=COMMANDS,
        desc="""
        This extension point allows you to contribute commands that are
        executed when the interactive Python shell is started.

        e.g. Each item in the list is a string of arbitrary Python code::

          'import os, sys'
          'from traits.api import *'

        Yes, I know this is insecure but it follows the usual Python rule of
        'we are all consenting adults'.
        """,
    )

    #### Contributions to extension points made by this plugin ################

    # Bindings.
    contributed_bindings = List(contributes_to=BINDINGS)
    tasks = List(contributes_to=TASKS)

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def start(self):
        logger.debug("started python shell plugin")

    def _contributed_bindings_default(self):
        """
        By default, expose the Envisage application object to the namespace
        """
        return [{"application": self.application}]

    def _tasks_default(self):
        return [
            TaskFactory(
                id="envisage.plugins.tasks.python_shell_task",
                name="Python Shell",
                factory=EnvisagePythonShellTask,
            ),
        ]
