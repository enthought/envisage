""" An extension point. """


# Standard library imports.
import inspect, weakref

# Enthought library imports.
from enthought.traits.api import TraitType, Undefined, implements

# Local imports.
from i_extension_point import IExtensionPoint


class ExtensionPoint(TraitType):
    """ An extension point. """

    # Even though trait types do not themselves have traits, we can still
    # declare that we implement an interface.
    implements(IExtensionPoint)
    
    #### 'ExtensionPoint' *CLASS* interface ###################################

    # The extension registry that is used by all extension points.
    extension_registry = None

    ###########################################################################
    # 'ExtensionPoint' *CLASS* interface.
    ###########################################################################

    @staticmethod
    def connect_extension_point_traits(obj):
        """ Connect all of the 'ExtensionPoint' traits on an object. """

        for trait_name, trait in obj.traits(__extension_point__=True).items():
            trait.trait_type.connect(obj, trait_name)

        return
    
    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, trait_type=None, id=None, **metadata):
        """ Constructor. """

        # We add '__extension_point_id__' to the metadata to make the extension
        # point traits easier to find.
        super(ExtensionPoint, self).__init__(
            __extension_point__=True, **metadata
        )

        # The trait type that describes the extension point.
        #
        # If we are handed a trait type *class* e.g. List, instead of a trait
        # type *instance* e.g. List() or List(Int) etc, then we just
        # instantiate it.
        if inspect.isclass(trait_type):
            trait_type = trait_type()
                
        self.trait_type = trait_type

        # The Id of the extension point.
        if id is None:
            self.id = '%s.%s' % (type(self).__module__, type(self).__name__)

        else:
            self.id = id

        # A dictionary that basically just keeps a reference to all extension
        # point listeners alive until their associated objects are garbage
        # collected.
        self._obj_to_listener_map = weakref.WeakKeyDictionary()

        return

    ###########################################################################
    # 'TraitType' interface.
    ###########################################################################

    def get(self, obj, trait_name):
        """ Trait type getter. """
        
        extensions = self._get_extensions(self.id)
        extensions = self._validate_extensions(obj, trait_name, extensions)

        return extensions

    def set(self, obj, name, value):
        """ Trait type setter. """

        self._set_extensions(self.id, value)

        return

    ###########################################################################
    # 'ExtensionPoint' interface.
    ###########################################################################

    def connect(self, obj, trait_name):
        """ Connect the extension point to a trait on an object.

        This allows the object to react to changes to the contributions to
        an extension point.

        fixme: It would be nice to be able to do this wiring up automatically,
        but we need a slight twek to traits to allow the trait type to get
        called when an instance is created.

        """

        def listener(extension_registry, event):
            """ Listener called when an extension point is changed. """

            # If an index was specified then we fire an '_items' changed
            # event.
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

        # Add the listener to the extension registry.
        extension_registry = ExtensionPoint.extension_registry
        extension_registry.add_extension_point_listener(listener)

        # Save a reference to the listener so that it does not get garbage
        # collected until its associated object is.
        listeners = self._obj_to_listener_map.setdefault(obj, [])
        listeners.append(listener)

        return
        
    ###########################################################################
    # Protected 'ExtensionPoint' interface.
    ###########################################################################

    def _get_extensions(self, extension_point_id):
        """ Return all contributions to this extension point. """

        extension_registry = ExtensionPoint.extension_registry

        return extension_registry.get_extensions(extension_point_id)

    def _set_extensions(self, extension_point_id, extensions):
        """ Set the contributions to this extension point. """

        extension_registry = ExtensionPoint.extension_registry

        if not hasattr(extension_registry, 'set_extensions'):
            raise SystemError('extension points cannot be set')
        
        extension_registry.set_extensions(extension_point_id, extensions)

        return

    def _validate_extensions(self, obj, trait_name, extensions):
        """ Validate the contibutions to this extension point. """

        # fixme: Ideally, instead of checking for 'None' here, we would just
        # make the trait type default to 'Any'. Unfortunately, the 'Any'
        # trait type doesn't support the 'TraitType' interface 8^( It doesn't
        # have a 'validate' method!
        if self.trait_type is not None:
            extensions = self.trait_type.validate(obj, trait_name, extensions)

        return extensions

#### EOF ######################################################################
