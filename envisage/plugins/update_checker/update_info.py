

from traits.api import Callable, HasTraits, List, Str



class VersionInfo(HasTraits):
    """ Represents the information about a particular version of an
    application.
    """

    # The version string that this
    version = Str()

    # Customer-facing notes about this version.  Typically this is an
    # HTML document containing the changelog between this version and
    # the previous version
    notes = Str()

    # The location of where to obtain this version.  Typically this will
    # be an HTTP URL, but this can be a URI for a local or LAN item, or
    # it can be a
    location = Str()

    # A function that takes a string (self.version) and returns something
    # that can be used to compare against the version-parsed version of
    # another VersionInfo object.
    version_parser = Callable()

    def __cmp__(self, other):
        """ Allows for comparing two VersionInfo objects so they can
        be presented in version-sorted order.  This is where we parse
        and interpretation of the **version** string attribute.
        """
        # TODO: Do something more intelligent here
        if self.version_parser is not None:
            self_ver = self.version_parser(self.version)
        else:
            self_ver = self.version
        if other.version_parser is not None:
            other_ver = other.version_parser(other.version)
        else:
            other_ver = other.version
        return self_ver < other_ver

class UpdateInfo(HasTraits):
    """ Encapsulates the information about the available update or
    updates.  An update can consist of multiple versions, with each
    version containing its own information and download URL.
    """

    updates = List(VersionInfo)

    pass




