""" The default extension registry implementation. """


# Standard library imports.
import inspect, logging, types

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

    def get_extensions(self, extension_point, **kw):
        """ Return all contributions to an extension point. """
        
        extensions = []
        for plugin in self.application.plugin_manager.plugins:
            extensions.extend(self._harvest_methods(plugin, extension_point))
            extensions.extend(self._harvest_traits(plugin, extension_point))

        logger.debug('extensions to %s are %s', extension_point, extensions)

        return extensions

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _harvest_methods(self, plugin, extension_point):
        """ Harvest all method-based contributions. """

        extensions = []
        for name, value in inspect.getmembers(plugin):
            if self._is_extension_method(value, extension_point):
                result = getattr(plugin, name)(self.application)
                if not isinstance(result, list):
                    result = [result]
                            
                extensions.extend(result)

        return extensions

    def _harvest_traits(self, plugin, extension_point):
        """ Harvest all trait-based contributions. """

        extensions = []

        for trait_name in plugin.traits(extension_point=extension_point):
            value = getattr(plugin, trait_name)
            if not isinstance(value, list):
                value = [value]

            extensions.extend(value)

        return extensions

    def _is_extension_method(self, value, extension_point):
        """ Return True if the value is an extension method.

        i.e. If the method is one that makes a contribution to an extension
        point. Currently there is exactly one way to make a method make a
        contribution, and that is to mark it using the 'extension_point'
        decorator, e.g::

          @extension_point('acme.motd.messages')
          def get_messages(self, application):
              ...
              return some_messages

        """

        if inspect.ismethod(value):
            if extension_point == getattr(value, '__extension_point__', None):
                return True

        return False

#### EOF ######################################################################
