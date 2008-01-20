""" The developer plugin. """


# Enthought library imports.
from enthought.envisage.api import Plugin
from enthought.traits.api import Instance


class DeveloperPlugin(Plugin):
    """ The developer plugin.

    This plugin contains the non-GUI part of the tools that (hopefully) help
    developers to inspect and debug a running Envisage workbench application.

    """

    # Extension points Ids.
    #PERSPECTIVES = 'enthought.envisage.ui.workbench.perspectives'
    #VIEWS        = 'enthought.envisage.ui.workbench.views'

    #### 'IPlugin' interface ##################################################

    id   = 'enthought.envisage.developer'
    name = 'Developer'

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
        'enthought.envisage.developer.charm.api.CodeBrowser', service=True
    )
    
    ###########################################################################
    # 'DeveloperPlugin' interface.
    ###########################################################################

    def _code_browser_default(self):
        """ Trait initializer. """

        from enthought.envisage.developer.charm.api import CodeBrowser
        
        return CodeBrowser()


if __name__ == '__main__':
    from enthought.envisage.developer.ui.api import browse_plugin
    browse_plugin(DeveloperPlugin)
    
#### EOF ######################################################################
