# (C) Copyright 2007-2026 Enthought, Inc., Austin, TX
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
from traits.api import Instance, Property, provides, Str
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
        logger.info(
            "plugin {} has no Id - using <{}>".format(
                object.__repr__(self), id
            )
        )

        return id

    def _name_default(self):
        """Trait initializer."""

        name = camel_case_to_words(type(self).__name__)
        logger.info(
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

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __repr__(self):
        """String representation of a Plugin object"""
        return f"{type(self).__name__}(id={self.id!r}, name={self.name!r})"
