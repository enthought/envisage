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

    # The Ids of the plugins that must be started before this one is started.
    requires = List(Str)

    #### Private interface ####################################################

    # The Ids of the services that were automatically registered.
    _service_ids = List

    ###########################################################################
    # 'IExtensionProvider' interface.
    ###########################################################################

    def get_extension_points(self):
        """ Return the extension points offered by the provider.

        The return value *must* be alist. Return an empty list if the provider
        does not offer any extension points.

        """

        extension_points = []
        for trait in self.traits().values():
            if isinstance(trait.trait_type, ExtensionPoint):
                extension_points.append(trait.trait_type)

        return extension_points

    def get_extensions(self, extension_point_id):
        """ Return the provider's extensions to an extension point.

        The return value *must* be a list. Return an empty list if the provider
        does not contribute any extensions to the extension point.

        """

        return self._harvest_traits(extension_point_id)

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

        from extension_point_binding import initialize_extension_point_traits
        initialize_extension_point_traits(self)
        
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

    def _harvest_traits(self, extension_point_id):
        """ Harvest all trait-based contributions to an extension point. """

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

#### EOF ######################################################################
