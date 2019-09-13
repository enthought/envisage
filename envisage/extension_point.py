# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" A trait type used to declare and access extension points. """


# Standard library imports.
import inspect, weakref

# Enthought library imports.
from traits.api import List, TraitType, Undefined, provides

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
INVALID_TRAIT_TYPE = 'extension points must be "List"s e.g. List, List(Int)' \
' but a value of %s was specified.'


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
        metadata['__extension_point__'] = True
        super(ExtensionPoint, self).__init__(**metadata)

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
            raise ValueError('an extension point must have an Id')

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
        return "ExtensionPoint(id={})".format(self.id)

    ###########################################################################
    # 'TraitType' interface.
    ###########################################################################

    def get(self, obj, trait_name):
        """ Trait type getter. """

        extension_registry = self._get_extension_registry(obj)

        # Get the extensions to this extension point.
        extensions = extension_registry.get_extensions(self.id)

        # Make sure the contributions are of the appropriate type.
        return self.trait_type.validate(obj, trait_name, extensions)

    def set(self, obj, name, value):
        """ Trait type setter. """

        extension_registry = self._get_extension_registry(obj)

        # Note that some extension registry implementations may not support the
        # setting of extension points (the default, plugin extension registry
        # for exxample ;^).
        extension_registry.set_extensions(self.id, value)

        return

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
            """ Listener called when an extension point is changed. """

            # If an index was specified then we fire an '_items' changed event.
            if event.index is not None:
                name = trait_name + '_items'
                old  = Undefined
                new  = event

            # Otherwise, we fire a normal trait changed event.
            else:
                name = trait_name
                old  = event.removed
                new  = event.added

            obj.trait_property_changed(name, old, new)

            return

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

        extension_registry = getattr(obj, 'extension_registry', None)
        if extension_registry is None:
            raise ValueError(
                'The "ExtensionPoint" trait type can only be used in '
                'objects that have a reference to an extension registry '
                'via their "extension_registry" trait. '
                'Extension point Id <%s>' % self.id
            )

        return extension_registry

#### EOF ######################################################################
