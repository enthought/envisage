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
            # Harvest all method-based contributions.
            extensions.extend(
                self._get_method_extensions(plugin, extension_point)
            )

            # Harvest all trait-based contributions.
            extensions.extend(
                self._get_trait_extensions(plugin, extension_point)
            )

        logger.debug('extensions to %s are %s', extension_point, extensions)

        return extensions

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_method_extensions(self, plugin, extension_point):
        """ Harvest all method-based contributions. """

        extensions = []
        for name, value in type(plugin).__dict__.items():
            if self._is_extension(value, extension_point):
                result = getattr(plugin, name)(self.application)
                if not isinstance(result, list):
                    result = [result]
                            
                extensions.extend(result)

        return extensions

    def _get_trait_extensions(self, plugin, extension_point):
        """ Harvest all trait-based contributions. """

        extensions = []

        for trait_name in plugin.traits(extension_point=extension_point):
            value = getattr(plugin, trait_name)
            if not isinstance(value, list):
                value = [value]

            extensions.extend(value)

        return extensions
        
    def _is_extension(self, value, extension_point):
        """ Return True if a value is an extension to an extension point. """

        if type(value) is types.FunctionType:
            if self._has_matching_decorator(value, extension_point):
                return True

            if self._has_matching_name(value, extension_point):
                return True

        return False

    def _has_matching_decorator(self, fn, extension_point):
        """ Return True if the function has a matching decorator. """

        return extension_point == getattr(fn, '__extension_point__', None)

    def _has_matching_name(self, fn, extension_point):
        """ Return True if the function's name matches the extension point.

        The comparison is done on the function name with any undescores ('_')
        replaced with periods ('.').

        e.g, If a plugin has a method named::

          def enthought_envisage_ui_workbench_views(self, application):
              ...

        Then the name used in the comparison is::

          'enthought.envisage.ui.workbench.views'
          
        """

        return extension_point == fn.func_name.replace('_', '.')
        
#### EOF ######################################################################
