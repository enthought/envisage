""" A trait type for a value that is found in a preference. """


# Standard library imports.
import inspect

# Enthought library imports.
from enthought.traits.api import List, TraitError, TraitType


class Preference(TraitType):
    """ A trait type for a value that is found in a preference. """

    #### 'ExtensionPoint' *CLASS* interface ###################################

    # The preferences node (or service) that contains the preferences.
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

        return self.preferences.get(path, self.trait_type.default_value)

    def set(self, obj, name, value):
        """ Trait type setter. """

        path = self._get_path(obj, name)
        
        return self.preferences.set(path, value)

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_path(self, obj, name):
        """ Return the path to the preferences node. """

        if self.path is not None:
            path = self.path

        else:
            path = '%s.%s' % (obj.PREFERENCES, name)

        return path
    
#### EOF ######################################################################
