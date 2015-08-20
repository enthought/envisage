""" Classes used to represent packages. """


# Standard library imports.
from os.path import join

# Enthought library imports.
from apptools.io.api import File
from traits.api import Instance, List, Str

# Local imports.
from .namespace import Namespace


class Package(Namespace):
    """ A package. """

    #### 'Package' interface ##################################################

    # The namespace that the package is defined in.
    #
    # fixme: This is always None for packages so why should we have this trait!
    # If I remember correctly it is something to do with trait identification!
    namespace = Instance(Namespace)

    # The package contents (modules and sub-packages).
    contents = List

    # The absolute filename of the package.
    filename = Str

    # The package name.
    name = Str

    # The package's parent package (None if this is a top level package).
    parent = Instance('Package')

    ###########################################################################
    # 'Package' interface.
    ###########################################################################

    def create_sub_package(self, name):
        """ Creates a sub-package with the specified name. """

        sub_package = File(join(self.filename, name))
        sub_package.create_package()

        return

    def delete_sub_package(self, name):
        """ Deletes the sub-package with the specified name. """

        sub_package = File(join(self.filename, name))
        sub_package.delete()

        return

    ###########################################################################
    # Private interface
    ###########################################################################

    def _name_changed(self, name):
        """ Called when the package name has been changed. """

        ##print '**** Package name changed', self.name

        return

#### EOF ######################################################################
