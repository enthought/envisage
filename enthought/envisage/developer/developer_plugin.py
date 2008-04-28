""" The developer plugin. """


# Enthought library imports.
from enthought.envisage.api import Plugin, ServiceFactory
from enthought.traits.api import List


# The package that this module is in.
PKG = '.'.join(__name__.split('.')[:-1])


class DeveloperPlugin(Plugin):
    """ The developer plugin.

    This plugin contains the non-GUI part of the tools that (hopefully) help
    developers to inspect and debug a running Envisage workbench application.

    """

    # The Ids of the extension points that this plugin contributes to.
    SERVICE_FACTORIES = 'enthought.envisage.service_factories'

    #### 'IPlugin' interface ##################################################

    # The plugin's globally unique identifier.
    id = 'enthought.envisage.developer'

    # The plugin's name (suitable for displaying to the user).
    name = 'Developer'

    #### Extension points offered by this plugin ##############################

    # None.

    #### Contributions to extension points made by this plugin ################

    service_factories = List(contributes_to=SERVICE_FACTORIES)
    
    def _service_factories_default(self):
        """ Trait initializer. """

        code_browser_class = PKG + '.code_browser.api.CodeBrowser'
        
        code_browser_service_factory = ServiceFactory(
            protocol = code_browser_class,
            factory  = code_browser_class,
            scope    = 'application'
        )

        return [code_browser_service_factory]
    
#### EOF ######################################################################
