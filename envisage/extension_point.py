# (C) Copyright 2007-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" A trait type used to declare and access extension points. """


# Standard library imports.
import inspect
import warnings
import weakref

# Enthought library imports.
from traits.api import List, TraitType, Undefined, provides
from traits.trait_list_object import TraitList

# Local imports.
from .i_extension_point import IExtensionPoint


def contributes_to(id):
    """ A factory for extension point decorators!

    As an alternative to making contributions via traits, you can use this
    decorator to mark any method on a 'Plugin' as contributing to an extension
    point (note this is *only* used on 'Plugin' instances!).

    e.g. Using a trait you might have something like::

        class MyPlugin(Plugin):
            messages = List(contributes_to='acme.messages')

            def _messages_default(self):
                return ['Hello', 'Hola']

    whereas, using the decorator, it would be::

        class MyPlugin(Plugin):
            @contributes_to('acme.messages')
            def _get_messages(self):
                return ['Hello', 'Hola']

    There is not much in it really, but the decorator version looks a little
    less like 'magic' since it doesn't require the developer to know about
    Traits default initializers. However, if you know that you will want to
    dynamically change your contributions then use the trait version  because
    all you have to do is change the value of the trait and the framework will
    react accordingly.

    """

    def decorator(fn):
        """ A decorator for marking methods as extension contributors. """

        fn.__extension_point__ = id

        return fn

    return decorator


# Exception message template.
INVALID_TRAIT_TYPE = (
    'extension points must be "List"s e.g. List, List(Int)'
    " but a value of %s was specified."
)


# Even though trait types do not themselves have traits, we can still
# declare that we implement an interface.
@provides(IExtensionPoint)
class ExtensionPoint(TraitType):
    """ A trait type used to declare and access extension points.

    Note that this is a trait *type* and hence does *NOT* have traits itself
    (i.e. it does *not* inherit from 'HasTraits').

    """

    ###########################################################################
    # 'ExtensionPoint' *CLASS* interface.
    ###########################################################################

    @staticmethod
    def bind(obj, trait_name, extension_point_id):
        """ Create a binding to an extension point. """

        from .extension_point_binding import bind_extension_point

        return bind_extension_point(obj, trait_name, extension_point_id)

    @staticmethod
    def connect_extension_point_traits(obj):
        """ Connect all of the 'ExtensionPoint' traits on an object. """

        for trait_name, trait in obj.traits(__extension_point__=True).items():
            trait.trait_type.connect(obj, trait_name)

        return

    @staticmethod
    def disconnect_extension_point_traits(obj):
        """ Disconnect all of the 'ExtensionPoint' traits on an object. """

        for trait_name, trait in obj.traits(__extension_point__=True).items():
            trait.trait_type.disconnect(obj, trait_name)

        return

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, trait_type=List, id=None, **metadata):
        """ Constructor. """

        # We add '__extension_point__' to the metadata to make the extension
        # point traits easier to find with the 'traits' and 'trait_names'
        # methods on 'HasTraits'.
        metadata["__extension_point__"] = True
        super().__init__(**metadata)

        # The trait type that describes the extension point.
        #
        # If we are handed a trait type *class* e.g. List, instead of a trait
        # type *instance* e.g. List() or List(Int) etc, then we instantiate it.
        if inspect.isclass(trait_type):
            trait_type = trait_type()

        # Currently, we only support list extension points (we may in the
        # future want to allow other collections e.g. dictionaries etc).
        if not isinstance(trait_type, List):
            raise TypeError(INVALID_TRAIT_TYPE % trait_type)

        self.trait_type = trait_type

        # The Id of the extension point.
        if id is None:
            raise ValueError("an extension point must have an Id")

        self.id = id

        # A dictionary that is used solely to keep a reference to all extension
        # point listeners alive until their associated objects are garbage
        # collected.
        #
        # Dict(weakref.ref(Any), Dict(Str, Callable))
        self._obj_to_listeners_map = weakref.WeakKeyDictionary()

        return

    def __repr__(self):
        """ String representation of an ExtensionPoint object """
        return "ExtensionPoint(id={!r})".format(self.id)

    ###########################################################################
    # 'TraitType' interface.
    ###########################################################################

    def get(self, obj, trait_name):
        """ Trait type getter. """
        cache_name = self._get_cache_name(trait_name)
        if cache_name not in obj.__dict__:
            self._update_cache(obj, trait_name)

        value = obj.__dict__[cache_name]
        # validate again
        self.trait_type.validate(obj, trait_name, value[:])
        return value

    def set(self, obj, name, value):
        """ Trait type setter. """

        extension_registry = self._get_extension_registry(obj)

        # Note that some extension registry implementations may not support the
        # setting of extension points (the default, plugin extension registry
        # for exxample ;^).
        extension_registry.set_extensions(self.id, value)

    ###########################################################################
    # 'ExtensionPoint' interface.
    ###########################################################################

    def connect(self, obj, trait_name):
        """ Connect the extension point to a trait on an object.

        This allows the object to react when contributions are added or
        removed from the extension point.

        fixme: It would be nice to be able to make the connection automatically
        but we would need a slight tweak to traits to allow the trait type to
        be notified when a new instance that uses the trait type is created.

        """

        def listener(extension_registry, event):
            """ Listener called when an extension point is changed.

            Parameters
            ----------
            extension_registry : IExtensionRegistry
                Registry that maintains the extensions.
            event : ExtensionPointChangedEvent
                Event for created for the change.
                If the event.index is None, this means the entire extensions
                is set to a new value. If the event.index is not None, some
                portion of the list has been modified.
            """
            if event.index is not None:
                # We know where in the list is changed.

                # Mutate the _ExtensionPointValue to fire ListChangeEvent
                # expected from observing item change.
                getattr(obj, trait_name)._sync_values(event)

                # For on_trait_change('name_items')
                obj.trait_property_changed(
                    trait_name + "_items", Undefined, event
                )

            else:
                # The entire list has changed. We reset the cache and fire a
                # normal trait changed event.
                self._update_cache(obj, trait_name)

        # In case the cache was created first and the registry is then mutated
        # before this ``connect``` is called, the internal cache would be in
        # an inconsistent state. This also has the side-effect of firing
        # another change event, hence allowing future changes to be observed
        # without having to access the trait first.
        self._update_cache(obj, trait_name)

        extension_registry = self._get_extension_registry(obj)

        # Add the listener to the extension registry.
        extension_registry.add_extension_point_listener(listener, self.id)

        # Save a reference to the listener so that it does not get garbage
        # collected until its associated object does.
        listeners = self._obj_to_listeners_map.setdefault(obj, {})
        listeners[trait_name] = listener

        return

    def disconnect(self, obj, trait_name):
        """ Disconnect the extension point from a trait on an object. """

        extension_registry = self._get_extension_registry(obj)

        listener = self._obj_to_listeners_map[obj].get(trait_name)
        if listener is not None:
            # Remove the listener from the extension registry.
            extension_registry.remove_extension_point_listener(
                listener, self.id
            )

            # Clean up.
            del self._obj_to_listeners_map[obj][trait_name]

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_extension_registry(self, obj):
        """ Return the extension registry in effect for an object. """

        extension_registry = getattr(obj, "extension_registry", None)
        if extension_registry is None:
            raise ValueError(
                'The "ExtensionPoint" trait type can only be used in '
                "objects that have a reference to an extension registry "
                'via their "extension_registry" trait. '
                "Extension point Id <%s>" % self.id
            )

        return extension_registry

    def _get_cache_name(self, trait_name):
        """ Return the cache name for the extension point value associated
        with a given trait.
        """
        return "__envisage_{}".format(trait_name)

    def _update_cache(self, obj, trait_name):
        """ Update the internal cached value for the extension point and
        fire change event.

        Parameters
        ----------
        obj : HasTraits
            The object on which an ExtensionPoint is defined.
        trait_name : str
            The name of the trait for which ExtensionPoint is defined.
        """
        cache_name = self._get_cache_name(trait_name)
        old = obj.__dict__.get(cache_name, Undefined)
        new = (
            _ExtensionPointValue(
                _get_extensions(obj, trait_name),
                object=obj,
                name=trait_name,
            )
        )
        obj.__dict__[cache_name] = new
        obj.trait_property_changed(trait_name, old, new)


class _ExtensionPointValue(TraitList):
    """ _ExtensionPointValue is the list being returned while retrieving the
    attribute value for an ExtensionPoint trait.

    This list returned for an ExtensionPoint acts as a proxy to query
    extensions in an ExtensionRegistry for a given extension point id. Users of
    ExtensionPoint expect to handle a list-like object, and expect to be able
    to listen to "mutation" on the list. The ExtensionRegistry remains to be
    the source of truth as to what extensions are available for a given
    extension point ID.

    Users are not expected to mutate the list directly. All mutations to
    extensions are expected to go through the extension registry to maintain
    consistency. With that, all methods for mutating the list are nullified,
    unless it is used internally.

    The requirement to support ``observe("name:items")`` means this list,
    associated with `name`, cannot be a property that gets recomputed on every
    access (enthought/traits/#624), it needs to be cached. As with any
    cached quantity, it needs to be synchronized with the ExtensionRegistry.

    The assumption on the internal values being synchronized with the registry
    breaks down if the extension registry is mutated before listeners
    are hooked up between the extension point and the registry. This sequence
    of events is difficult to enforce. Therefore we always resort to the
    extension registry for querying values.

    Parameters
    ----------
    iterable : iterable
        Iterable providing the items for the list
    obj : HasTraits
        The object on which an ExtensionPoint is defined.
    trait_name : str
        The name of the trait for which ExtensionPoint is defined.
    """

    def __init__(self, iterable=(), *, object, name):
        """ Reimplemented TraitList.__init__

        Parameters
        ----------
        object : HasTraits
            The object on which an ExtensionPoint is defined.
        trait_name : str
            The name of the trait for which ExtensionPoint is defined.
        """
        super().__init__(iterable)

        # Flag to control access for mutating the list. Only internal
        # code can mutate the list. See _sync_values
        self._internal_use = False

        self._object = object
        self._name = name

    def __eq__(self, other):
        if self._internal_use:
            return super().__eq__(other)
        return _get_extensions(self._object, self._name) == other

    def __getitem__(self, key):
        if self._internal_use:
            return super().__getitem__(key)
        return _get_extensions(self._object, self._name)[key]

    def __len__(self):
        if self._internal_use:
            return super().__len__()
        return len(_get_extensions(self._object, self._name))

    def _sync_values(self, event):
        """ Given an ExtensionPointChangedEvent, modify the values in this list
        to match. This is an internal method only used by Envisage code.

        Parameters
        ----------
        event : ExtenstionPointChangedEvent
            Event being fired for extension point values changed (typically
            via the extension registry)
        """
        self._internal_use = True
        try:
            if isinstance(event.index, slice):
                if event.added:
                    self[event.index] = event.added
                else:
                    del self[event.index]
            else:
                slice_ = slice(
                    event.index, event.index + len(event.removed)
                )
                self[slice_] = event.added
        finally:
            self._internal_use = False

    # Reimplement TraitList interface to avoid any mutation.
    # The original implementation of __setitem__ and __delitem__ can be used
    # by internal code.

    def __delitem__(self, key):
        """ Reimplemented TraitList.__delitem__ """

        # This is used by internal code

        if not self._internal_use:
            warnings.warn(
                "Extension point cannot be mutated directly.",
                RuntimeWarning,
                stacklevel=2,
            )
            return

        super().__delitem__(key)

    def __iadd__(self, value):
        """ Reimplemented TraitList.__iadd__ """
        # We should not need it for internal use either.
        warnings.warn(
            "Extension point cannot be mutated directly.",
            RuntimeWarning,
            stacklevel=2,
        )
        return self[:]

    def __imul__(self, value):
        """ Reimplemented TraitList.__imul__ """
        # We should not need it for internal use either.
        warnings.warn(
            "Extension point cannot be mutated directly.",
            RuntimeWarning,
            stacklevel=2,
        )
        return self[:]

    def __setitem__(self, key, value):
        """ Reimplemented TraitList.__setitem__ """

        # This is used by internal code

        if not self._internal_use:
            warnings.warn(
                "Extension point cannot be mutated directly.",
                RuntimeWarning,
                stacklevel=2,
            )
            return

        super().__setitem__(key, value)

    def append(self, object):
        """ Reimplemented TraitList.append """
        # We should not need it for internal use either.
        warnings.warn(
            "Extension point cannot be mutated directly.",
            RuntimeWarning,
            stacklevel=2,
        )

    def clear(self):
        """ Reimplemented TraitList.clear """
        # We should not need it for internal use either.
        warnings.warn(
            "Extension point cannot be mutated directly.",
            RuntimeWarning,
            stacklevel=2,
        )

    def extend(self, iterable):
        """ Reimplemented TraitList.extend """
        # We should not need it for internal use either.
        warnings.warn(
            "Extension point cannot be mutated directly.",
            RuntimeWarning,
            stacklevel=2,
        )

    def insert(self, index, object):
        """ Reimplemented TraitList.insert """
        # We should not need it for internal use either.
        warnings.warn(
            "Extension point cannot be mutated directly.",
            RuntimeWarning,
            stacklevel=2,
        )

    def pop(self, index=-1):
        """ Reimplemented TraitList.pop """
        # We should not need it for internal use either.
        warnings.warn(
            "Extension point cannot be mutated directly.",
            RuntimeWarning,
            stacklevel=2,
        )

    def remove(self, value):
        """ Reimplemented TraitList.remove """
        # We should not need it for internal use either.
        warnings.warn(
            "Extension point cannot be mutated directly.",
            RuntimeWarning,
            stacklevel=2,
        )

    def reverse(self):
        """ Reimplemented TraitList.reverse """
        # We should not need it for internal use either.
        warnings.warn(
            "Extension point cannot be mutated directly.",
            RuntimeWarning,
            stacklevel=2,
        )

    def sort(self, *, key=None, reverse=False):
        """ Reimplemented TraitList.sort """
        # We should not need it for internal use either.
        warnings.warn(
            "Extension point cannot be mutated directly.",
            RuntimeWarning,
            stacklevel=2,
        )


def _get_extensions(object, name):
    """ Return the extensions reported by the extension registry for the
    given object and the name of a trait whose type is an ExtensionPoint.

    Parameters
    ----------
    object : HasTraits
        Object on which an ExtensionPoint is defined
    name : str
        Name of the trait whose trait type is an ExtensionPoint.

    Returns
    -------
    extensions : list
        All the extensions for the extension point.
    """
    extension_point = object.trait(name).trait_type
    extension_registry = extension_point._get_extension_registry(object)

    # Get the extensions to this extension point.
    return extension_registry.get_extensions(extension_point.id)
