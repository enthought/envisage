""" A mutable, manually populated extension registry used for testing. """


# Enthought library imports.
from envisage.api import ExtensionRegistry, UnknownExtension


class MutableExtensionRegistry(ExtensionRegistry):
    """ A mutable, manually populated extension registry used for testing. """

    ###########################################################################
    # 'MutableExtensionRegistry' interface.
    ###########################################################################

    def add_extension(self, extension_point_id, extension):
        """ Contribute an extension to an extension point. """

        self.add_extensions(extension_point_id, [extension])

        return

    def add_extensions(self, extension_point_id, extensions):
        """ Contribute a list of extensions to an extension point. """

        self._check_extension_point(extension_point_id)

        old   = self._get_extensions(extension_point_id)
        index = len(old)
        old.extend(extensions)

        # Let any listeners know that the extensions have been added.
        refs = self._get_listener_refs(extension_point_id)
        self._call_listeners(refs, extension_point_id, extensions, [], index)

        return

    def remove_extension(self, extension_point_id, extension):
        """ Remove a contribution from an extension point. """

        self.remove_extensions(extension_point_id, [extension])

        return

    def remove_extensions(self, extension_point_id, extensions):
        """ Remove a list of contributions from an extension point. """

        for extension in extensions:
            try:
                self._get_extensions(extension_point_id).remove(extension)

            except ValueError:
                raise UnknownExtension(extension_point_id, extension)

        # Let any listeners know that the extensions have been removed.
        refs = self._get_listener_refs(extension_point_id)
        self._call_listeners(refs, extension_point_id, [], extensions, None)

        return

#### EOF ######################################################################
