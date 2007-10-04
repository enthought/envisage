""" The default implementation of the 'IPlugin' interface. """


# Standard library imports.
import inspect, logging

# Enthought library imports.
from enthought.traits.api import HasTraits, Instance, List, Str, implements

# Local imports.
from extension_provider import ExtensionProvider
from extension_point import ExtensionPoint
from i_application import IApplication
from i_plugin import IPlugin


# Logging.
logger = logging.getLogger(__name__)


class Plugin(ExtensionProvider):
    """ The default implementation of the 'IPlugin' interface.

    This class is intended to be subclasses for each plugin that you create.

    """

    implements(IPlugin)

    #### 'IPlugin' interface ##################################################
    
    # The application that the plugin is part of.
    application = Instance(IApplication)

    # A description of what the plugin is and does.
    description = Str

    # The plugin's unique identifier.
    id = Str

    # The plugin's name (suitable for displaying to the user).
    name = Str

    # The Ids of the plugins that must be started before this one is started
    # (this is usually because this plugin requires a service that the other
    # plugin starts).
    requires = List(Str)

    #### Private interface ####################################################

    # The Ids of the services that were automatically registered.
    _service_ids = List
    
    ###########################################################################
    # 'IExtensionProvider' interface.
    ###########################################################################

    def get_extension_points(self):
        """ Return the extension points offered by the provider.

        The return value *,ust* be alist. Return an empty list if the provider
        does not offer any extension points.

        """

        extension_points = []
        for trait in self.traits().values():
            if isinstance(trait.trait_type, ExtensionPoint):
                extension_points.append(trait.trait_type.id)

        return extension_points

    def get_extensions(self, extension_point):
        """ Return the provider's extensions to an extension point.

        The return value *must* be a list. Return an empty list if the provider
        does not contribute any extensions to the extension point.

        """

        extensions = self._harvest_methods(extension_point)
        extensions.extend(self._harvest_traits(extension_point))

        return extensions

    ###########################################################################
    # 'IServiceProvider' interface.
    ###########################################################################

    def register_services(self):
        """ Register the services offered by the provider. """

        application = self.application
        for trait_name, trait in self.traits(service=True).items():
            # If a specific protocol was specified then use it.
            if trait.service_protocol is not None:
                protocol = trait.service_protocol

            # Otherwise, use the type of the objects that can be assigned to
            # the trait.
            #
            # fixme: This works for 'Instance' traits, but what about the
            # 'AdaptsTo' and 'AdaptedTo' traits?
            else:
                trait_type = trait.trait_type
                
                # The 'Instance' trait type allows the class to be specified
                # as a string.
                klass = trait_type.klass
                if isinstance(klass, basestring):
                    protocol = trait_type.find_class(klass)

                else:
                    protocol = klass

            # The service provider can decide not to register the service by
            # returning None.
            service = getattr(self, trait_name)
            if service is not None:
                # When we register the service we save the service Id so that
                # we can unregister it later.
                service_id = application.register_service(protocol, service)
                self._service_ids.append(service_id)
                       
        return

    def unregister_services(self):
        """ Unregister any service offered by the provider. """

        for service_id in self._service_ids:
            self.application.unregister_service(service_id)

        return
    
    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _id_default(self):
        """ Initializer. """

        return '%s.%s' % (type(self).__module__, type(self).__name__)
    
    #### Methods ##############################################################
 
    def start(self):
        """ Start the plugin. """

        self.register_services()

        return

    def stop(self):
        """ Stop the plugin. """

        self.unregister_services()

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handlers ################################################

    def _anytrait_changed(self, trait_name, old, new):
        """ Static trait change handler. """

        # Ignore the '_items' part of the trait name (if it is there!).
        base_trait_name = trait_name.split('_items')[0]
        trait           = self.trait(base_trait_name)

        # Is this a contribution trait?
        if trait.extension_point is not None:
            if trait_name.endswith('_items'):
                removed = new.removed
                added   = new.added
                index   = new.index
                
            else:
                removed = old
                added   = new
                index   = 0
                
            # Let the extension registry know about the change.
            self._fire_extensions_changed(
                trait.extension_point, added, removed, index=index
            )

        return
        
    #### Methods ##############################################################
    
    def _harvest_methods(self, extension_point):
        """ Harvest all method-based contributions. """

        extensions = []
        for name, value in inspect.getmembers(self):
            if self._is_extension_method(value, extension_point):
                result = getattr(self, name)()
                if not isinstance(result, list):
                    result = [result]
                            
                extensions.extend(result)

        return extensions

    def _harvest_traits(self, extension_point):
        """ Harvest all trait-based contributions. """

        extensions = []
        for trait_name in self.trait_names(extension_point=extension_point):
            value = getattr(self, trait_name)
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
              messages = [...]
              ...
              return messages

        """

        if inspect.ismethod(value):
            if extension_point == getattr(value, '__extension_point__', None):
                return True

        return False
    
#### EOF ######################################################################
