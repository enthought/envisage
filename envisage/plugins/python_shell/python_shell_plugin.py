# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" The interactive Python shell plugin. """


# Enthought library imports.
from envisage.api import ExtensionPoint, Plugin
from traits.api import Dict, List, Str


class PythonShellPlugin(Plugin):
    """ The interactive Python shell plugin. """

    # Extension point Ids.
    BINDINGS = 'envisage.plugins.python_shell.bindings'
    COMMANDS = 'envisage.plugins.python_shell.commands'
    VIEWS    = 'envisage.ui.workbench.views'

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'envisage.plugins.python_shell'

    # The plugin's name (suitable for displaying to the user).
    name = 'Python Shell'

    #### Extension points offered by this plugin ##############################

    bindings = ExtensionPoint(
        List(Dict), id=BINDINGS, desc="""

        This extension point allows you to contribute name/value pairs that
        will be bound when the interactive Python shell is started.

        e.g. Each item in the list is a dictionary of name/value pairs::

        {'x' : 10, 'y' : ['a', 'b', 'c']}

        """
    )

    commands = ExtensionPoint(
        List(Str), id=COMMANDS, desc="""

        This extension point allows you to contribute commands that are
        executed when the interactive Python shell is started.

        e.g. Each item in the list is a string of arbitrary Python code::

          'import os, sys'
          'from traits.api import *'

        Yes, I know this is insecure but it follows the usual Python rule of
        'we are all consenting adults'.

        """
    )

    #### Contributions to extension points made by this plugin ################

    # Bindings.
    contributed_bindings = List(contributes_to=BINDINGS)

    def _contributed_bindings_default(self):
        """ Trait initializer. """

        return [{'application' : self.application}]

    # Views.
    contributed_views = List(contributes_to=VIEWS)

    def _contributed_views_default(self):
        """ Trait initializer. """

        # Local imports.
        from .view.python_shell_view import PythonShellView
        from .view.namespace_view import NamespaceView

        return [PythonShellView, NamespaceView]

#### EOF ######################################################################
