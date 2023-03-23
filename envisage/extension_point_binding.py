# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" A binding between a trait on an object and an extension point. """


# Enthought library imports.
from traits.api import Any, HasTraits, Instance, Str, Undefined

# Local imports.
from .i_extension_registry import IExtensionRegistry


class ExtensionPointBinding(HasTraits):
    """A binding between a trait on an object and an extension point."""

    #### 'ExtensionPointBinding' *CLASS* interface ############################

    # Global dictionary used to keep ExtensionPointBinding objects alive.
    _bindings = {}

    #### 'ExtensionPointBinding' interface ####################################

    # The object that we are binding the extension point to.
    obj = Any

    # The Id of the extension point.
    extension_point_id = Str

    # The extension registry used by the binding. If this trait is not set then
    # the class-scope extension registry set on the 'ExtensionPoint' class is
    # used (and if that is not set then the binding won't work ;^)
    extension_registry = Instance(IExtensionRegistry)

    # The name of the trait that we are binding the extension point to.
    trait_name = Str

    #### Private interface ####################################################

    # A flag that prevents us from setting a trait twice.
    _event_handled = False

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """Constructor."""

        super().__init__(**traits)

        # Initialize the object's trait from the extension point.
        self._set_trait(notify=False)

        # Wire-up the trait change and extension point handlers.
        self._bind()

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handlers ################################################

    def _on_trait_changed(self, obj, trait_name, old, new):
        """Dynamic trait change handler."""

        if not self._event_handled:
            self._set_extensions(new)

    def _on_trait_items_changed(self, obj, trait_name, old, event):
        """Dynamic trait change handler."""

        if not self._event_handled:
            self._set_extensions(getattr(obj, self.trait_name))

    #### Other observer pattern listeners #####################################

    def _extension_point_listener(self, extension_registry, event):
        """Listener called when an extension point is changed."""

        self._event_handled = True
        if event.index is not None:
            self._update_trait(event)

        else:
            self._set_trait(notify=True)
        self._event_handled = False

    #### Methods ##############################################################

    def _bind(self):
        """Wire-up trait change handlers etc."""

        # Listen for the object's trait being changed.
        self.obj.on_trait_change(self._on_trait_changed, self.trait_name)

        self.obj.on_trait_change(
            self._on_trait_items_changed, self.trait_name + "_items"
        )

        # Listen for the extension point being changed.
        self.extension_registry.add_extension_point_listener(
            self._extension_point_listener, self.extension_point_id
        )

    def _unbind(self):
        """Undo the effects of _bind"""

        self.extension_registry.remove_extension_point_listener(
            self._extension_point_listener, self.extension_point_id
        )

        self.obj.on_trait_change(
            self._on_trait_items_changed,
            self.trait_name + "_items",
            remove=True,
        )

        self.obj.on_trait_change(
            self._on_trait_changed, self.trait_name, remove=True
        )

    def _set_trait(self, notify):
        """Set the object's trait to the value of the extension point."""

        value = self.extension_registry.get_extensions(self.extension_point_id)
        traits = {self.trait_name: value}

        self.obj.trait_set(trait_change_notify=notify, **traits)

    def _update_trait(self, event):
        """Update the object's trait to the value of the extension point."""

        self._set_trait(notify=False)

        self.obj.trait_property_changed(
            self.trait_name + "_items", Undefined, event
        )

    def _set_extensions(self, extensions):
        """Set the extensions to an extension point."""

        self.extension_registry.set_extensions(
            self.extension_point_id, extensions
        )


# Factory function for creating bindings.
def bind_extension_point(
    obj, trait_name, extension_point_id, extension_registry
):
    """Create a binding to an extension point.

    The returned ExtensionPointBinding object is also stored in a (private)
    global dictionary, so that users aren't required to keep a reference to it.
    That global dictionary entry can be removed with a matching call to
    unbind_extension_point.

    Parameters
    ----------
    obj : HasTraits
        The HasTraits object that we're binding to
    trait_name : str
        The name of the trait on obj to bind to.
    extension_point_id : str
        The id of the extension point.
    extension_registry : IExtensionRegistry
        The extension registry that the extension point is registered to.

    Returns
    -------
    ExtensionPointBinding
        An object that manages the binding.
    """

    binding = ExtensionPointBinding(
        obj=obj,
        trait_name=trait_name,
        extension_point_id=extension_point_id,
        extension_registry=extension_registry,
    )

    # Keep a reference to each binding in the ExtensionPointBinding._bindings
    # global dictionary. Without this, the binding would become inactive
    # if the caller didn't keep a reference.
    bindings = ExtensionPointBinding._bindings.setdefault(obj, [])
    bindings.append(binding)
    return binding


def unbind_extension_point(
    obj, trait_name, extension_point_id, extension_registry
):
    """
    Remove an extension point binding.

    Changes to extension point contributions will no longer affect the target
    trait. Also removes the matching ExtensionPointBinding object from the
    global dictionary.

    Parameters
    ----------
    obj : HasTraits
        The HasTraits object that we're binding to
    trait_name : str
        The name of the trait on obj to bind to.
    extension_point_id : str
        The id of the extension point.
    extension_registry : IExtensionRegistry
        The extension registry that the extension point is registered to.
    """
    # Find the corresponding binding in the global dict.
    bindings = ExtensionPointBinding._bindings

    # Find the matching ExtensionPointBinding object. Search in reverse order,
    # since that's most likely to give the right binding quickly under the
    # normal first-in-last-out pattern for nested setup and teardown.
    index, binding = next(
        (index, binding)
        for index, binding in reversed(list(enumerate(bindings[obj])))
        if binding.trait_name == trait_name
        if binding.extension_point_id == extension_point_id
        if binding.extension_registry == extension_registry
    )

    # Remove the binding from the global dict, and remove the dict entry
    # altogether if it's now empty.
    bindings[obj].pop(index)
    if not bindings[obj]:
        bindings.pop(obj)

    # Undo the binding
    binding._unbind()
