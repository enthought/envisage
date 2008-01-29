""" The developer plugin. """


# Enthought library imports.
from enthought.envisage.api import Plugin
from enthought.traits.api import Instance


class DeveloperPlugin(Plugin):
    """ The developer plugin.

    This plugin contains the non-GUI part of the tools that (hopefully) help
    developers to inspect and debug a running Envisage workbench application.

    """

    #### 'IPlugin' interface ##################################################

    # The plugin's globally unique identifier.
    id = 'enthought.envisage.developer'

    # The plugin's name (suitable for displaying to the user).
    name = 'Developer'

    #### 'DeveloperPlugin' interface ##########################################

    ###########################################################################
    # Extension points offered by this plugin.
    ###########################################################################

    # None
    
    ###########################################################################
    # Contributions to extension points made by this plugin.
    ###########################################################################

    # None

    ###########################################################################
    # Services offered by this plugin.
    ###########################################################################

    # A code browser.
    code_browser = Instance(
        'enthought.envisage.developer.code_browser.api.CodeBrowser',
        service=True
    )
    
    ###########################################################################
    # 'DeveloperPlugin' interface.
    ###########################################################################

    def _code_browser_default(self):
        """ Trait initializer. """

        from enthought.envisage.developer.code_browser.api import CodeBrowser

        # fixme: The code browser should persist the code database in an
        # area set-aside for the plugin (maybe 'plugin.home' to mirror
        # 'application.home'?).
        return CodeBrowser()
    
#### EOF ######################################################################
