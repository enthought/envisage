""" The interface for extension registries. """


# Enthought library imports.
from enthought.traits.api import Interface


class IExtensionRegistry(Interface):
    """ The interface for extension registries. """

    def add_extension(self, extension_point, extension):
        """ Contribute an extension to an extension point.

        If the extension point has not previously been added to the registry
        then it is added automatically here.
        
        """

    def add_extensions(self, extension_point, extensions):
        """ Contribute a list of extensions to an extension point.

        If the extension point has not previously been added to the registry
        then it is added automatically here.

        """

    def add_extension_point(self, extension_point):
        """ Add an extension point.

        """

    def add_extension_listener(self, listener, extension_point=None):
        """ Add a listener for extensions being added or removed.

        If an extension point is specified then the listener will only called
        when extensions are added to or removed from that extension point (the
        extension point may or may not have been added to the registry at the
        time of this call).
        
        If no extension point is specified then the listener will be called
        when extensions are added to or removed from *any* extension point.

        When extensions are added or removed all specific listeners are called
        (in arbitrary order), followed by all non-specific listeners (again, in
        arbitrary order).
        
        """
        
    def add_extension_points(self, extension_points):
        """ Add a list of extension points.

        """

    def get_extensions(self, extension_point, **kw):
        """ Return a list containing all contributions to an extension point.

        Return an empty list if the extension point does not exist.

        The keyword arguments can be used to pass arguments that are required
        by individual concrete implementations.

        """

    def get_extension_points(self):
        """ Return all extension points.

        """

    def remove_extension(self, extension_point, extension):
        """ Remove a contribution from an extension point.

        Raises a 'ValueError' if the extension does not exist.

        """

    def remove_extensions(self, extension_point, extensions):
        """ Remove a list of contributions from an extension point.

        Raises a 'ValueError' if any of the extensions does not exist.
        
        """

    def remove_extension_listener(self, listener, extension_point=None):
        """ Remove a listener for extensions being added/removed.

        Raises a 'ValueError' if the listener does not exist.

        """

    def remove_extension_point(self, extension_point):
        """ Remove an extension point.

        Raises a 'KeyError' if the extension point does not exist.

        """

    def remove_extension_points(self, extension_point):
        """ Remove an extension point.

        Raises a 'KeyError' if any of the extension points do not exist.

        """

#### EOF ######################################################################
