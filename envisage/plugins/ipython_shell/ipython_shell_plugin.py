""" An IPython shell plugin. """


# Enthought library imports.
from envisage.api import ExtensionPoint, Plugin
from traits.api import Dict, List, Str


class IPythonShellPlugin(Plugin):
    """ An IPython shell plugin. """

    # Extension point Ids.
    BANNER          = 'envisage.plugins.ipython_shell.banner'
    BINDINGS        = 'envisage.plugins.python_shell.bindings'
    COMMANDS        = 'envisage.plugins.python_shell.commands'
    VIEWS           = 'envisage.ui.workbench.views'
    ACTION_SETS     = 'envisage.ui.workbench.action_sets'

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'envisage.plugins.python_shell'

    # The plugin's name (suitable for displaying to the user).
    name = 'Python Shell'

    #### Extension points offered by this plugin ##############################

    banner = ExtensionPoint(
        List(Str), id=BANNER, desc="""

        This extension point allows you to contribute a string that
        is printed as a banner when the IPython shell is started.
        """
    )


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

    # Our action sets.
    action_sets = List(contributes_to=ACTION_SETS)

    def _action_sets_default(self):
        """ Trait initializer. """
        from envisage.plugins.ipython_shell.actions.ipython_shell_actions \
            import IPythonShellActionSet
        return [IPythonShellActionSet]

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
        from .view.ipython_shell_view import IPythonShellView
        from .view.namespace_view \
                    import NamespaceView

        return [IPythonShellView, NamespaceView]

#### EOF ######################################################################
