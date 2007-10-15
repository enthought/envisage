""" A connection between a trait on an object and an extension point. """


# Standard library imports.
import weakref

# Enthought library imports.
from enthought.traits.api import Any, HasTraits, Str, Undefined


class ExtensionPointConnection(HasTraits):
    """ A connection between a trait on an object and an extension point. """

    #### 'ExtensionPointConnection' *CLASS* interface #########################

    # The extension registry that is used by all extension point connections.
    extension_registry = None # Instance(IExtensionRegistry)

    # We keep a reference to each connection alive until its associated object
    # is garbage collected.
    _connections = weakref.WeakKeyDictionary()
    
    #### 'ExtensionPointConnection' interface #################################

    # The object that we are connecting the extension point to.
    obj = Any
    
    # The Id of the extension point.
    extension_point_id = Str

    # The name of the trait that we are connecting the extension point to.
    trait_name = Str
    
    #### Private interface ####################################################

    # A flag that prevents us from setting a trait twice.
    _event_handled = False

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Constructor. """

        super(ExtensionPointConnection, self).__init__(**traits)

        # Initialize the object's trait from the extension point.
        self._set_trait(notify=False)

        # Wire-up the trait change and extension point handlers.
        self._initialize()

        # We keep a reference to each connection alive until its associated
        # object is garbage collected.
        ExtensionPointConnection._connections[self.obj] = self

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handlers ################################################

    def _on_trait_changed(self, obj, trait_name, old, new):
        """ Dynamic trait change handler. """

        if not self._event_handled:
            self._set_extensions(new)

        return

    def _on_trait_items_changed(self, obj, trait_name, old, event):
        """ Dynamic trait change handler. """

        if not self._event_handled:
            self._set_extensions(getattr(obj, self.trait_name))

        return

    #### Other observer pattern listeners #####################################
    
    def _extension_point_listener(self, extension_registry, event):
        """ Listener called when an extension point is changed. """

        self._event_handled = True
        if event.index is not None:
            self._update_trait(event)
            
        else:
            self._set_trait(notify=True)
        self._event_handled = False

        return

    #### Methods ##############################################################

    def _initialize(self):
        """ Wire-up trait change handlers etc. """

        # Listen for the object's trait being changed.
        self.obj.on_trait_change(
            self._on_trait_changed, self.trait_name
        )

        self.obj.on_trait_change(
            self._on_trait_items_changed, self.trait_name + '_items'
        )

        # Listen for the extension point being changed.
        self.extension_registry.add_extension_point_listener(
            self._extension_point_listener, self.extension_point_id
        )

        return

    def _set_trait(self, notify):
        """ Set the object's trait to the value of the extension point. """

        value = self.extension_registry.get_extensions(self.extension_point_id)
        traits = {self.trait_name : value}

        self.obj.set(trait_change_notify=notify, **traits)

        return

    def _update_trait(self, event):
        """ Update the object's trait to the value of the extension point. """

        self._set_trait(notify=False)

        self.obj.trait_property_changed(
            self.trait_name + '_items', Undefined, event
        )

        return

    def _set_extensions(self, extensions):
        """ Set the extensions to an extension point. """
        
        self.extension_registry.set_extensions(
            self.extension_point_id, extensions
        )

        return


def connect_extension_point(obj, trait_name, extension_point_id):
    """ Create a connection to an extension point. """

    connection = ExtensionPointConnection(
        obj                = obj,
        trait_name         = trait_name,
        extension_point_id = extension_point_id
    )

    return connection

#### EOF ######################################################################
