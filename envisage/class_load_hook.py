# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" A hook to allow code be executed when a class is loaded. """


# Standard library imports.
import sys

# Enthought library imports.
from traits.api import Callable, HasTraits, MetaHasTraits, Str


class ClassLoadHook(HasTraits):
    """ A hook to allow code to be executed when a class is loaded.

    If the class is *already* loaded when the 'connect' method is called then
    the code is executed immediately.

    """

    #### 'ClassLoadHook' interface ############################################

    # The name of the class. When this class is loaded the 'on_class_loaded'
    # method is called.
    class_name = Str

    # A callable that will be executed when the class is loaded. The callable
    # must take a single argument which will be the loaded class.
    #
    # This is used in the default implementation of 'on_class_loaded'. If you
    # override that, then you don't have to set to this trait.
    on_load = Callable

    ###########################################################################
    # 'ClassLoadHook' interface.
    ###########################################################################

    def connect(self):
        """ Connect the load hook to listen for the class being loaded. """

        MetaHasTraits.add_listener(self.on_class_loaded, self.class_name)

        # If the class has already been loaded then run the code now!
        cls = self._get_class(self.class_name)
        if cls is not None:
            self.on_class_loaded(cls)

        return

    def disconnect(self):
        """ Disconnect the load hook. """

        MetaHasTraits.remove_listener(self.on_class_loaded, self.class_name)

        return

    def on_class_loaded(self, cls):
        """ This method is called when the class is loaded.

        If 'self.on_load' is not None, it calls 'self.on_load(cls)'.

        """

        if self.on_load is not None:
            self.on_load(cls)

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_class(self, class_path):
        """ Returns the class defined by *class_path*.

        Returns **None** if the class has not yet been loaded.

        """

        # Only check if the class name has at least a partial hierarchy.
        #
        # fixme: Comment should say why!
        if '.' in class_path:
            components = class_path.split('.')

            module_name = '.'.join(components[:-1])
            class_name  = components[-1]

            # The class is loaded if its module has been imported and the class
            # is defined in the module dictionary.
            module = sys.modules.get(module_name, None)
            if module is not None and hasattr(module, class_name):
                klass = getattr(module, class_name)

            else:
                klass = None

        else:
            klass = None

        return klass

#### EOF ######################################################################
