""" A binding between a trait on an object and an extension point. """


# Enthought library imports.
from enthought.traits.api import Any, HasTraits, Str, Undefined


class ExtensionPointBinding(HasTraits):
    """ A binding between a trait on an object and an extension point. """

    #### 'ExtensionPointBinding' *CLASS* interface ############################

    # The extension registry that is used by all extension point bindingss.
    extension_registry = None
    
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
        self._initialize(self.extension_registry)

        # Listen for the trait being changed.
        self.obj.on_trait_change(self._on_trait_changed, self.trait_name)

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handlers ################################################

    def _on_trait_changed(self, obj, trait_name, old, new):
        """ Dynamic trait change handler. """

        if not self._event_handled:
            raise SystemError(
                'cannot set extension point %s' % self.extension_point
            )

        return

    #### Other observer pattern listeners #####################################
    
    def _extension_point_changed_listener(
        self, registry, extension_point, added, removed
    ):
        """ Listener called when an extension point is changed. """

        extensions = registry.get_extensions(self.extension_point)

        self._event_handled = True
        setattr(self.obj, self.trait_name, extensions)
        self._event_handled = False

        return

    #### Methods ##############################################################

    def _initialize(self, extension_registry):
        """ Initialize the object's traits from the extension registry. """
        
        value  = extension_registry.get_extensions(self.extension_point)
        traits = {self.trait_name : value}

        self.obj.set(trait_change_notify=False, **traits)

        extension_registry.add_extension_listener(
            self._extension_point_changed_listener, self.extension_point
        )

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
