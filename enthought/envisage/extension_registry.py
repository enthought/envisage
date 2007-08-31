""" The default extension registry implementation. """


# Standard library imports.
import logging, types

# Enthought library imports.
from enthought.traits.api import HasTraits, Instance, implements

# Local imports.
from i_application import IApplication
from i_extension_registry import IExtensionRegistry


# Logging.
logger = logging.getLogger(__name__)


class ExtensionRegistry(HasTraits):
    """ The default extension registry implementation. """

    implements(IExtensionRegistry)

    #### 'ExtensionRegistry' interface ########################################

    # The application that the registry is part of.
    application = Instance(IApplication)
    
    ###########################################################################
    # 'IExtensionRegistry' interface.
    ###########################################################################

    def get_extensions(self, extension_point):
        """ Return all contributions to an extension point. """
        
        extensions = []
        for plugin in self.application.plugin_manager.plugins:
            for name, value in type(plugin).__dict__.items():
                if self._is_extension(value, extension_point):
                    result = getattr(plugin, name)(self.application)
                    if type(result) is not list:
                        result = [result]
                            
                    extensions.extend(result)
                        
        logger.debug('extensions to %s are %s', extension_point, extensions)

        return extensions

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _is_extension(self, value, extension_point):
        """ Return True if a value is an extension to an extension point. """

        if type(value) is not types.FunctionType:
            return False
        
        id = getattr(value, '__extension_point__', None)
        if id == extension_point:
            return True

        if value.func_name.replace('_', '.') == extension_point:
            return True

        return False
        
#### EOF ######################################################################
