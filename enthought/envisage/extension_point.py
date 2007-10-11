""" An extension point. """


# Standard library imports.
import inspect, weakref

# Enthought library imports.
from enthought.traits.api import List, TraitError, TraitType, Undefined
from enthought.traits.api import implements

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

    #### Private 'ExtensionPoint' *CLASS* interface ###########################

    # A dictionary of all extension point traits.
    #
    # { obj : trait_names }
    _obj_to_trait_names_map = weakref.WeakKeyDictionary()

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, trait_type=None, id=None, **metadata):
        """ Constructor. """

        super(ExtensionPoint, self).__init__(**metadata)

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

        return

    ###########################################################################
    # 'TraitType' interface.
    ###########################################################################

    def get(self, obj, trait_name):
        """ Trait type getter. """

        extensions = self._get_extensions(self.id)
        extensions = self._validate_extensions(obj, trait_name, extensions)

        # If this is the first time that this trait type instance has been
        # accessed then we add ourselves as a listener for when the extension
        # point is changed.
        if len(self._obj_to_trait_names_map) == 0:
            ExtensionPoint.extension_registry.add_extension_point_listener(
                self._extension_point_listener, self.id
            )
            
        # We save the object and trait name combination so that we can fire the
        # appropriate trait events if the extension point is changed in the
        # extension registry.
        trait_names = self._obj_to_trait_names_map.setdefault(obj, {})
        if not trait_name in trait_names:
            trait_names[trait_name] = True

        return extensions

    def set(self, obj, name, value):
        """ Trait type setter. """

        self._set_extensions(self.id, value)

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

    ###########################################################################
    # Private 'ExtensionPoint' interface.
    ###########################################################################

    def _extension_point_listener(self, extension_registry, event):
        """ Listener called when an extension point is changed. """

        for obj, trait_names in self._obj_to_trait_names_map.items():
            for trait_name in trait_names:
                # If an index was specified then we fire an '_items' changed
                # event.
                if event.index is not None:
                    trait_name += '_items'
                    old        = Undefined
                    new        = event

                # Otherwise, we fire a normal trait changed event.
                else:
                    old        = event.removed
                    new        = event.added

                obj.trait_property_changed(trait_name, old, new)
        
        return
    
#### EOF ######################################################################
