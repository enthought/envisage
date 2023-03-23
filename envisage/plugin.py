# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The default implementation of the 'IPlugin' interface. """

# Standard library imports.
import logging
import os
from os.path import exists, join

# Enthought library imports.
from traits.api import Instance, List, Property, provides, Str
from traits.util.camel_case import camel_case_to_words

# Local imports.
from .extension_point import ExtensionPoint
from .extension_provider import ExtensionProvider
from .i_application import IApplication
from .i_extension_point_user import IExtensionPointUser
from .i_extension_registry import IExtensionRegistry
from .i_plugin import IPlugin
from .i_plugin_activator import IPluginActivator
from .i_service_registry import IServiceRegistry
from .i_service_user import IServiceUser
from .plugin_activator import PluginActivator

# Logging.
logger = logging.getLogger(__name__)


@provides(IPlugin, IExtensionPointUser, IServiceUser)
class Plugin(ExtensionProvider):
    """The default implementation of the 'IPlugin' interface.

    This class is intended to be subclassed for each plugin that you create.

    """

    #### 'IPlugin' interface ##################################################

    #: The activator used to start and stop the plugin.
    #:
    #: By default the *same* activator instance is used for *all* plugins of
    #: this type.
    activator = Instance(IPluginActivator, PluginActivator())

    #: The application that the plugin is part of.
    application = Instance(IApplication)

    #: The name of a directory (created for you) that the plugin can read and
    #: write to at will.
    home = Str

    #: The plugin's unique identifier.
    #:
    #: If no identifier is specified then the module and class name of the
    #: plugin are used to create an Id with the form 'module_name.class_name'.
    id = Str

    #: The plugin's name (suitable for displaying to the user).
    #:
    #: If no name is specified then the plugin's class name is used with an
    #: attempt made to turn camel-case class names into words separated by
    #: spaces (e.g. if the class name is 'MyPlugin' then the name would be
    #: 'My Plugin'). Of course, if you really care about the actual name, then
    #: just set it!
    name = Str

    #### 'IExtensionPointUser' interface ######################################

    #: The extension registry that the object's extension points are stored in.
    extension_registry = Property(Instance(IExtensionRegistry))

    #### 'IServiceUser' interface #############################################

    #: The service registry that the object's services are stored in.
    service_registry = Property(Instance(IServiceRegistry))

    #### Private interface ####################################################

    # The Ids of the services that were automatically registered.
    _service_ids = List

    ###########################################################################
    # 'IExtensionPointUser' interface.
    ###########################################################################

    def _get_extension_registry(self):
        """Trait property getter."""

        return self.application

    ###########################################################################
    # 'IServiceUser' interface.
    ###########################################################################

    def _get_service_registry(self):
        """Trait property getter."""

        return self.application

    ###########################################################################
    # 'IExtensionProvider' interface.
    ###########################################################################

    def get_extension_points(self):
        """Return the extension points offered by the provider."""

        extension_points = [
            trait.trait_type
            for trait in self.traits(__extension_point__=True).values()
        ]

        return extension_points

    def get_extensions(self, extension_point_id):
        """Return the provider's extensions to an extension point."""

        # Each class can have at most *one* trait that contributes to a
        # particular extension point.
        #
        # fixme: We make this restriction in case that in future we can wire up
        # the list traits directly. If we don't end up doing that then it is
        # fine to allow mutiple traits!
        trait_names = self.trait_names(contributes_to=extension_point_id)

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

    def _home_default(self):
        """Trait initializer."""

        # Each plugin gets a sub-directory of a 'plugins' directory in
        # 'application.home'.
        #
        # i.e. .../my.application.id/plugins/
        plugins_dir = join(self.application.home, "plugins")
        if not exists(plugins_dir):
            os.mkdir(plugins_dir)

        # Now create the 'home' directory of this plugin.
        home_dir = join(plugins_dir, self.id)
        if not exists(home_dir):
            os.mkdir(home_dir)

        return home_dir

    def _id_default(self):
        """Trait initializer."""

        id = "%s.%s" % (type(self).__module__, type(self).__name__)
        logger.warning(
            "plugin {} has no Id - using <{}>".format(
                object.__repr__(self), id
            )
        )

        return id

    def _name_default(self):
        """Trait initializer."""

        name = camel_case_to_words(type(self).__name__)
        logger.warning(
            "plugin {} has no name - using <{}>".format(
                object.__repr__(self), name
            )
        )

        return name

    #### Methods ##############################################################

    def start(self):
        """Start the plugin.

        This method will *always* be empty so that you never have to call
        'super().start()' if you provide an implementation in a
        derived class.

        The framework does what it needs to do when it starts a plugin by means
        of the plugin's activator.

        """

        pass

    def stop(self):
        """Stop the plugin.

        This method will *always* be empty so that you never have to call
        'super().stop()' if you provide an implementation in a
        derived class.

        The framework does what it needs to do when it stops a plugin by means
        of the plugin's activator.

        """

        pass

    ###########################################################################
    # 'Plugin' interface.
    ###########################################################################

    def connect_extension_point_traits(self):
        """Connect all of the plugin's extension points.

        This means that the plugin will be notified if and when contributions
        are add or removed.

        """

        ExtensionPoint.connect_extension_point_traits(self)

    def disconnect_extension_point_traits(self):
        """Disconnect all of the plugin's extension points."""

        ExtensionPoint.disconnect_extension_point_traits(self)

    def register_services(self):
        """Register the services offered by the plugin."""

        for trait_name, trait in self.traits(service=True).items():
            logger.warning(
                'DEPRECATED: Do not use the "service=True" metadata anymore. '
                "Services should now be offered using the service "
                "offer extension point (envisage.service_offers) "
                "from the core plugin. "
                "Plugin %s trait <%s>" % (self, trait_name)
            )

            # Register a service factory for the trait.
            service_id = self._register_service_factory(trait_name, trait)

            # We save the service Id so that so that we can unregister the
            # service when the plugin is stopped.
            self._service_ids.append(service_id)

    def unregister_services(self):
        """Unregister any service offered by the plugin."""

        # Unregister the services in the reverse order that we registered
        # them.
        service_ids = self._service_ids[:]
        service_ids.reverse()

        for service_id in service_ids:
            try:
                self.application.get_service_from_id(service_id)
            except ValueError:
                # the service may have already been individually unregistered
                pass
            else:
                self.application.unregister_service(service_id)

        # Just in case the plugin is started again!
        self._service_ids = []

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handlers ################################################

    def _anytrait_changed(self, trait_name, old, new):
        """Static trait change handler."""

        # Ignore the '_items' part of the trait name (if it is there!), and get
        # the actual trait.
        base_trait_name = trait_name.split("_items")[0]
        trait = self.trait(base_trait_name)

        # If the trait is one that contributes to an extension point then fire
        # an appropriate 'extension point changed' event.
        if trait.contributes_to is not None:
            if trait_name.endswith("_items"):
                added = new.added
                removed = new.removed
                index = new.index

            else:
                added = new
                removed = old
                index = slice(0, len(old))

            # Let the extension registry know about the change.
            self._fire_extension_point_changed(
                trait.contributes_to, added, removed, index
            )

    #### Methods ##############################################################

    def _create_multiple_traits_exception(self, extension_point_id):
        """Create the exception raised when multiple traits are found."""

        exception = ValueError(
            "multiple traits for extension point <%s> in plugin <%s>"
            % (extension_point_id, self.id)
        )

        return exception

    def _get_extensions_from_trait(self, trait_name):
        """Return the extensions contributed via the specified trait."""

        try:
            extensions = getattr(self, trait_name)

        except Exception:
            logger.exception(
                "getting extensions from %s, trait <%s>" % (self, trait_name)
            )
            raise

        return extensions

    def _get_service_protocol(self, trait):
        """Determine the protocol to register a service trait with."""

        # If a specific protocol was specified then use it.
        if trait.service_protocol is not None:
            protocol = trait.service_protocol

        # Otherwise, use the type of the objects that can be assigned to the
        # trait.
        #
        # fixme: This works for 'Instance' traits, but what about 'AdaptsTo'
        # and 'Supports' traits?
        else:
            # Note that in traits the protocol can be an actual class or
            # interfacem or the *name* of a class or interface. This allows
            # us to lazy load them!
            protocol = trait.trait_type.klass

        return protocol

    def _register_service_factory(self, trait_name, trait):
        """Register a service factory for the specified trait."""

        # Determine the protocol that the service should be registered with.
        protocol = self._get_service_protocol(trait)

        # Register a factory for the service so that it will be lazily loaded
        # the first time somebody asks for a service with the same protocol
        # (this could obviously be a lambda function, but I thought it best to
        # be more explicit 8^).
        def factory(**properties):
            """A service factory."""

            return getattr(self, trait_name)

        return self.application.register_service(protocol, factory)

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __repr__(self):
        """String representation of a Plugin object"""
        return f"{type(self).__name__}(id={self.id!r}, name={self.name!r})"
