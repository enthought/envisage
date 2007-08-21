""" A trait type for a value that is found in a preference. """


# Standard library imports.
import inspect

# Enthought library imports.
from enthought.traits.api import CBool, CComplex, CFloat, CInt, CLong
from enthought.traits.api import Bool, Complex, Float, Int, Long, List
from enthought.traits.api import List, TraitType


# A mapping from non-casting trait types to their casting counterparts.
NON_CASTING_TO_CASTING_MAP = {
    Bool    : CBool,
    Complex : CComplex,
    Float   : CFloat,
    Int     : CInt,
    Long    : CLong,
}


class Preference(TraitType):
    """ A trait type for a value that is found in a preference. """

    #### 'ExtensionPoint' *CLASS* interface ###################################

    # The preferences node (or preferences service) that contains the
    # preferences.
    preferences = None
    
    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, trait_type, path=None, **metadata):
        """ Constructor. """

        super(Preference, self).__init__(**metadata)

        # The trait type that describes the extension point.
        #
        # If we are handed a trait type *class* e.g. List, instead of a trait
        # type *instance* e.g. List(Int), then we just instantiate it.
        if inspect.isclass(trait_type):
            trait_type = trait_type()
                
        self.trait_type = trait_type
        self.path       = path
        
        return

    ###########################################################################
    # 'TraitType' interface.
    ###########################################################################

    def get(self, obj, name):
        """ Trait type getter. """
 
        path = self._get_path(obj, name)

        # The raw value is always a string.
        raw = self.preferences.get(path, str(self.trait_type.default_value))

        # If the trait type is not 'Str' then try eval-ing the preference
        # value...
        casting = NON_CASTING_TO_CASTING_MAP.get(type(self.trait_type))
        if casting is not None:
            # fixme: We have to fudge it a little for booleans...
            #
            # bool('True')  -> True
            # bool('False') -> True
            #
            # This is because in Python a non-empty string is considered True
            # (the dodgy-old lazy boolean style of programming 8^(). This
            # leads to the slightly odd...
            #
            # bool(str(False)) -> True ;^)
            #
            # but:-
            #
            # eval('True')  -> True
            # eval('False') -> False
            #
            # So we use that instead.
            if casting is CBool:
                raw = eval(raw)

            # Now let the casting type do its thing.
            value = casting().validate(obj, name, raw)
            
        else:
            value = self.trait_type.validate(obj, name, raw)

        return value

    def set(self, obj, name, value):
        """ Trait type setter. """

        path = self._get_path(obj, name)
        
        return self.preferences.set(path, value)

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_path(self, obj, name):
        """ Return the path to the preferences value. """

        if self.path is not None:
            path = self.path

        else:
            path = self._get_preferences_path(obj, name)

        return path

    def _get_preferences_path(self, obj, name):
        """ Attempt to create a sensible preferences path for an object. """

        # If the object (or more usually, its class) has the path to a
        # preferences node defined explicitly then use that.
        path = getattr(obj, 'PREFERENCES', None)
        if path is None:
            # Otherwise, use the name of the package that the object's class is
            # defined in.
            path = self._get_package_name(type(obj))

        if len(path) > 0:
            path = '%s.%s' % (path, name)

        else:
            path = name

        return path

    def _get_package_name(self, klass):
        """ Return the name of the package that a class is defined in.

        e.g. For 'HasTraits' this would be 'enthought.traits'

        """

        module_name = klass.__module__

        components = module_name.split('.')
        if len(components) == 1:
            package_name = ''

        else:
            package_name = '.'.join(components[:-1])

        return package_name

#### EOF ######################################################################
