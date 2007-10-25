""" The default implementation of the 'IPlugin' interface. """


# Enthought library imports.
from enthought.traits.api import HasTraits, Instance, List, Str, implements

# Local imports.
from extension_provider import ExtensionProvider
from extension_point import ExtensionPoint
from i_application import IApplication
from i_plugin import IPlugin


class Plugin(ExtensionProvider):
    """ The default implementation of the 'IPlugin' interface.

    This class is intended to be subclassed for each plugin that you create.

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

    #### Private interface ####################################################

    # The Ids of the services that were automatically registered.
    _service_ids = List

    ###########################################################################
    # 'IExtensionProvider' interface.
    ###########################################################################

    def get_extension_points(self):
        """ Return the extension points offered by the provider. """

        extension_points = []
        for trait in self.traits(__extension_point__=True).values():
            extension_points.append(trait.trait_type)

        return extension_points

    def get_extensions(self, extension_point_id):
        """ Return the provider's extensions to an extension point. """

        # Each class can have at most *one* trait that contributes to a
        # particular extension point.
        #
        # fixme: We make this restriction in case that in future we can wire up
        # the list traits directly. If we don't end up doing that then it is
        # fine to allow mutiple traits!
        trait_names = self.trait_names(extension_point=extension_point_id)
        if len(trait_names) == 1:
            extensions = getattr(self, trait_names[0])

        elif len(trait_names) == 0:
            extensions = []

        else:
            raise self._create_multiple_traits_exception(extension_point_id)

        return extensions

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

        # Connect all of the plugin's extension point traits so that the plugin
        # will be notified if and when contributions are added or removed.
        ExtensionPoint.connect_extension_point_traits(self)

        # Register all service traits.
        self.register_services()

        return

    def stop(self):
        """ Stop the plugin. """

        # Unregister all service traits.
        self.unregister_services()

        return

    ###########################################################################
    # 'Plugin' interface.
    ###########################################################################

    def register_services(self):
        """ Register the services offered by the plugin. """

        application = self.application
        for trait_name, trait in self.traits(service=True).items():
            # Determine the protocol that the service should be registered
            # with.
            protocol = self._get_service_protocol(trait)

            # Register a factory for the service so that it will be lazily
            # loaded.
            def factory(protocol, properties):
                """ A service factory. """

                return getattr(self, trait_name)
            
            # When we register the service we save the service Id so that
            # we can unregister it later.
            service_id = application.register_service(protocol, factory)
            self._service_ids.append(service_id)
                       
        return

    def unregister_services(self):
        """ Unregister any service offered by the plugin. """

        for service_id in self._service_ids:
            self.application.unregister_service(service_id)

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

        if trait.extension_point is not None:
            if trait_name.endswith('_items'):
                added   = new.added
                removed = new.removed
                index   = new.index
                
            else:
                added   = new
                removed = old
                index   = slice(0, max(len(old), len(new)))
                
            # Let the extension registry know about the change.
            self._fire_extension_point_changed(
                trait.extension_point, added, removed, index
            )

        return
        
    #### Methods ##############################################################

    def _create_multiple_traits_exception(self, extension_point_id):
        """ Create the exception raised when multiple traits are found. """

        exception = ValueError(
            'multiple traits for extension point <%s> in plugin <%s>' % (
                extension_point_id, self.id
            )
        )
        
        return exception

    def _get_service_protocol(self, trait):
        """ Determine the protocol to register a service trait with. """
        
        # If a specific protocol was specified then use it.
        if trait.service_protocol is not None:
            protocol = trait.service_protocol

        # Otherwise, use the type of the objects that can be assigned to the
        # trait.
        #
        # fixme: This works for 'Instance' traits, but what about 'AdaptsTo'
        # and 'AdaptedTo' traits?
        else:
            # Note that in traits the protocol can be an actual class or
            # interfacem or the *name* of a class or interface. This allows
            # us to lazy load them!
            protocol = trait.trait_type.klass

        return protocol
    
#### EOF ######################################################################
