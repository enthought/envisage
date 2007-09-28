""" An extension point. """


# Standard library imports.
import inspect, weakref

# Enthought library imports.
from enthought.traits.api import List, TraitError, TraitType


def extension_point(id):
    """ A factory for extension point decorators! """

    def decorator(fn):
        """ A decorator for marking methods as extension contributors. """

        fn.__extension_point__ = id

        return fn

    return decorator


class ExtensionPoint(TraitType):
    """ An extension point. """

    #### 'ExtensionPoint' *CLASS* interface ###################################

    # The extension registry that is used by all extension points.
    extension_registry = None

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, trait_type=None, id=None, cached=True, **metadata):
        """ Constructor. """

        super(ExtensionPoint, self).__init__(**metadata)

        # The trait type that describes the extension point.
        #
        # If we are handed a trait type *class* e.g. List, instead of a trait
        # type *instance* e.g. List(Int), then we just instantiate it.
        if inspect.isclass(trait_type):
            trait_type = trait_type()
                
        self.trait_type = trait_type

        # The Id of the extension point.
        self.id = id or '%s.%s' % (type(self).__module__, type(self).__name__)

        # If the extension point is cached then extensions will be retreived
        # from the extension regsistry at most once.
        self.cached = cached

        # The cached extensions.
        self._cache = weakref.WeakKeyDictionary()
        
        return

    ###########################################################################
    # 'TraitType' interface.
    ###########################################################################

    def get(self, obj, name):
        """ Trait type getter. """

        if self.cached:
            all_traits = self._cache.setdefault(obj, {})
            if name in all_traits:
                extensions = all_traits[name]

            else:
                extensions = self._get_extensions(obj)
                extensions = self._validate_extensions(obj, name, extensions)

                all_traits[name] = extensions

        else:
            extensions = self._get_extensions(obj)
            extensions = self._validate_extensions(obj, name, extensions)

        return extensions

    def set(self, obj, name, value):
        """ Trait type setter. """
        
        raise TraitError('extension points cannot be set')

    ###########################################################################
    # Protected 'ExtensionPoint' interface.
    ###########################################################################

    def _get_extensions(self, obj):
        """ Return all contributions to this extension point. """

        extension_registry = ExtensionPoint.extension_registry

        return extension_registry.get_extensions(self.id)

    def _validate_extensions(self, obj, name, extensions):
        """ Validate the contibutions to this extension point. """

        # fixme: Ideally, instead of checking for 'None' here, we would just
        # make the trait type default to 'Any'. Unfortunately, the 'Any'
        # trait type doesn't support the 'TraitType' interface 8^( It doesn't
        # have a 'validate' method!
        if self.trait_type is not None:
            extensions = self.trait_type.validate(obj, name, extensions)

        return extensions
    
#### EOF ######################################################################
