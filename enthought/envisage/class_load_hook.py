""" A hook to allow code be executed when a class is loaded. """


# Enthought library imports.
from enthought.traits.api import Callable, HasTraits, MetaHasTraits, Str


class ClassLoadHook(HasTraits):
    """ A hook to allow code be executed when a class is loaded. """

    #### 'ClassLoadHook' interface ############################################
    
    # The name of the class. When this class is loaded the code in the hook
    # will be executed.
    class_name = Str

    # A callable that will be executed when the class is loaded. The callable
    # must take a single argument which will be the loaded class.
    #
    # This is used in the default implementation of 'on_class_loaded'. If you
    # override that, then  you don't have to set to this trait.
    on_load = Callable

    ###########################################################################
    # 'ClassLoadHook' interface.
    ###########################################################################

    def connect(self):
        """ Connect the load hook to listen for the class being loaded. """

        MetaHasTraits.add_listener(self.on_class_loaded, self.class_name)

        return

    def disconnect(self):
        """ Connect the load hook to listen for the class being loaded. """

        MetaHasTraits.remove_listener(self.on_class_loaded, self.class_name)

        return

    def on_class_loaded(self, cls):
        """ This method is called when the class is loaded.

        If 'self.on_load' is not None, it calls 'self.on_load(cls)'.

        """

        if self.on_load is not None:
            self.on_load(cls)

        return


class AdapterHook(ClassLoadHook):
    """ A class load hook that imports a module! """

    #### 'AdapterHook' interface ##############################################
    
    # The possibly dotted package path to the module that we want to import
    # when the class is loaded.
    module_name = Str

    ###########################################################################
    # 'ClassLoadHook' interface.
    ###########################################################################

    def on_class_loaded(self, cls):
        """ This method is called when the class is loaded. """

        exec "import %s" % self.module_name

        return

#### EOF ######################################################################
