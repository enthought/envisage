""" A binding between a trait on an object and an extension point. """


# Standard library imports.
import weakref

# Enthought library imports.
from enthought.traits.api import Any, HasTraits, Str


class ExtensionPointBinding(HasTraits):
    """ A binding between a trait on an object and an extension point. """

    #### 'ExtensionPointBinding' *CLASS* interface ############################

    # The extension registry that is used by all extension point bindingss.
    extension_registry = None # Instance(IExtensionRegistry)

    # We keep a reference to each binding alive until its associated object is
    # garbage collected.
    _bindings = weakref.WeakKeyDictionary()
    
    #### 'ExtensionPointBinding' interface ####################################

    # The object that we are binding the extension point to.
    obj = Any
    
    # The Id of the extension point.
    extension_point = Str

    # The name of the trait that we are binding the extension point to.
    trait_name = Str
    
    #### Private interface ####################################################

    # A flag that prevents us from setting a trait twice.
    _event_handled = False

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Constructor. """

        super(ExtensionPointBinding, self).__init__(**traits)

        # Initialize the object's trait from the extension point.
        self._set_trait(notify=False)

        # Wire-up the trait change and extension point handlers.
        self._initialize()

        # We keep a reference to each binding alive until its associated object
        # is garbage collected.
        ExtensionPointBinding._bindings[self.obj] = self

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handlers ################################################

    def _on_trait_changed(self, obj, trait_name, old, new):
        """ Dynamic trait change handler. """

        if not self._event_handled:
            self.extension_registry.set_extensions(self.extension_point, new)

        return

    #### Other observer pattern listeners #####################################
    
    def _extension_point_listener(self, extension_registry, event):
        """ Listener called when an extension point is changed. """

        self._event_handled = True
        self._set_trait(notify=True)
        self._event_handled = False

        return

    #### Methods ##############################################################

    def _initialize(self):
        """ Wire-up trait change handlers etc. """

        # Listen for the object's trait being changed.
        self.obj.on_trait_change(self._on_trait_changed, self.trait_name)

        # Listen for the extension point being changed.
        self.extension_registry.add_extension_listener(
            self._extension_point_listener, self.extension_point
        )

        return

    def _set_trait(self, notify):
        """ Set the object's trait to the value of the extension point. """

        value  = self.extension_registry.get_extensions(self.extension_point)
        traits = {self.trait_name : value}

        self.obj.set(trait_change_notify=notify, **traits)

        return


# Factory function for creating bindings.
def bind_extension_point(obj, trait_name, extension_point):
    """ Create a new extension point binding. """

    binding = ExtensionPointBinding(
        obj             = obj,
        trait_name      = trait_name,
        extension_point = extension_point
    )

    return binding

#### EOF ######################################################################
