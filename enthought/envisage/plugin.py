""" The default implementation of the 'IPlugin' interface. """


# Standard library imports.
import logging

# Enthought library imports.
from enthought.traits.api import Instance, List, Str, implements

# Local imports.
from extension_point import ExtensionPoint
from extension_provider import ExtensionProvider
from i_application import IApplication
from i_plugin import IPlugin
from i_plugin_activator import IPluginActivator
from plugin_activator import PluginActivator


# Logging.
logger = logging.getLogger(__name__)


def camel_case_to_words(s):
    """ Turn a string from CamelCase into words separated by spaces.

    e.g. 'CamelCase' -> 'Camel Case'

    """

    with_spaces = ''
    for i in range(len(s)):
        # We detect w word boundary if the character we are looking at is
        # upper case, but the character preceding it is lower case.
        if i > 0 and s[i].isupper() and s[i-1].islower():
            with_spaces += ' '

        with_spaces += s[i]

    return with_spaces


class Plugin(ExtensionProvider):
    """ The default implementation of the 'IPlugin' interface.

    This class is intended to be subclassed for each plugin that you create.

    """

    implements(IPlugin)

    #### 'IPlugin' interface ##################################################
    
    # The activator used to start and stop the plugin.
    #
    # By default the *same* activator instance is used for *all* plugins of
    # this type.
    activator = Instance(IPluginActivator, PluginActivator())

    # The application that the plugin is part of.
    application = Instance(IApplication)

    # The plugin's unique identifier.
    #
    # If no identifier is specified then the module and class name of the
    # plugin are used to create an Id with the form 'module_name.class_name'.
    id = Str

    # The plugin's name (suitable for displaying to the user).
    #
    # If no name is specified then the plugin's class name is used with an
    # attempt made to turn camel-case class names into words separated by
    # spaces (e.g. if the class name is 'MyPlugin' then the name would be
    # 'My Plugin'). Of course, if you really care about the actual name, then
    # just set it!
    name = Str

    #### Private interface ####################################################

    # The Ids of the services that were automatically registered.
    _service_ids = List

    ###########################################################################
    # 'IExtensionProvider' interface.
    ###########################################################################

    def get_extension_points(self):
        """ Return the extension points offered by the provider. """

        extension_points = [
            trait.trait_type

            for trait in self.traits(__extension_point__=True).values()
        ]
        
        return extension_points

    def get_extensions(self, extension_point_id):
        """ Return the provider's extensions to an extension point. """

        # Each class can have at most *one* trait that contributes to a
        # particular extension point.
        #
        # fixme: We make this restriction in case that in future we can wire up
        # the list traits directly. If we don't end up doing that then it is
        # fine to allow mutiple traits!
        trait_names = self._get_extension_trait_names(extension_point_id)
        if len(trait_names) == 0:
            extensions = []

        elif len(trait_names) == 1:
            extensions = self._get_extensions_from_trait(trait_names[0])
                
        else:
            raise self._create_multiple_traits_exception(extension_point_id)

        return extensions

    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _id_default(self):
        """ Trait initializer. """

        id = '%s.%s' % (type(self).__module__, type(self).__name__)
        logger.warn('plugin %s has no Id - using <%s>' % (self, id))
            
        return id

    def _name_default(self):
        """ Trait initializer. """

        name = camel_case_to_words(type(self).__name__)
        logger.warn('plugin %s has no name - using <%s>' % (self, name))

        return name
        
    #### Methods ##############################################################

    def start(self):
        """ Start the plugin.

        This method will *always* be empty so that you never have to call
        'super(xxx, self).start()' if you provide an implementation in a
        derived class.

        The framework does what it needs to do when it starts a plugin by means
        of the plugin's activator.

        """

        pass

    def stop(self):
        """ Stop the plugin.

        This method will *always* be empty so that you never have to call
        'super(xxx, self).stop()' if you provide an implementation in a
        derived class.

        The framework does what it needs to do when it stops a plugin by means
        of the plugin's activator.

        """

        pass

    ###########################################################################
    # 'Plugin' interface.
    ###########################################################################

    def connect_extension_point_traits(self):
        """ Connect all of the plugin's extesnion points.

        This means that the plugin will be notified if and when contributions
        are add or removed.

        """

        ExtensionPoint.connect_extension_point_traits(self)

        return

    def disconnect_extension_point_traits(self):
        """ Disconnect all of the plugin's extesnion points."""

        ExtensionPoint.disconnect_extension_point_traits(self)

        return
    
    def register_services(self):
        """ Register the services offered by the plugin. """

        for trait_name, trait in self.traits(service=True).items():
            # Register a service factory for the trait.
            service_id = self._register_service_factory(trait_name, trait)

            # We save the service Id so that so that we can unregister the
            # service when the plugin is stopped.
            self._service_ids.append(service_id)

        return

    def unregister_services(self):
        """ Unregister any service offered by the plugin. """

        # Unregister the services in the reverse order that we registered
        # them.
        service_ids = self._service_ids[:]
        service_ids.reverse()
        
        for service_id in service_ids:
            self.application.unregister_service(service_id)

        # Just in case the plugin is started again!
        self._service_ids = []
        
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

    def _get_extension_trait_names(self, extension_point_id):
        """ Return the names of traits that contribute to an extension point.

        fixme: Some people were confused by using 'extension_point=' when
        contributing to an extension point, so as an experiment we also allow
        'contributes_to='. Hopefully, one or other will win out and we can go
        back to having just one way of doing it!

        """

        trait_names = self.trait_names(extension_point=extension_point_id)
        if len(trait_names) > 0:
            logger.warn(
                'DEPRECATED: Use "contributes_to=", not "extension_point="'
            )
            
        trait_names += self.trait_names(contributes_to=extension_point_id)

        return trait_names
    
    def _get_extensions_from_trait(self, trait_name):
        """ Return the extensions contributed via the specified trait. """
        
        try:
            extensions = getattr(self, trait_name)

        except:
            logger.exception(
                'getting extensions from %s, trait <%s>' % (self, trait_name)
            )
            raise

        return extensions
    
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

    def _register_service_factory(self, trait_name, trait):
        """ Register a service factory for the specified trait. """
            
        # Determine the protocol that the service should be registered with.
        protocol = self._get_service_protocol(trait)
            
        # Register a factory for the service so that it will be lazily loaded
        # the first time somebody asks for a service with the same protocol
        # (this could obviously be a lambda function, but I thought it best to
        # be more explicit 8^).
        def factory(protocol, properties):
            """ A service factory. """

            return getattr(self, trait_name)

        return self.application.register_service(protocol, factory)
    
#### EOF ######################################################################
