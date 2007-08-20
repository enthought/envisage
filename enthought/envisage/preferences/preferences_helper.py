""" An object that can be initialized from a preference node. """


# Enthought library imports.
from enthought.traits.api import HasTraits, Str, Undefined


class PreferencesHelper(HasTraits):
    """ An object that can be initialized from a preferences node. """
    
    #### 'PreferencesHelper' interface ########################################

    # The path to the preference node that contains the preferences that we
    # use to initialize instances of this class.
    path = Str

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, preferences=None, **traits):
        """ Constructor. """
        
        super(PreferencesHelper, self).__init__(**traits)

        if preferences is not None:
            self.initialize(preferences)

        return

    ###########################################################################
    # 'PreferencesHelper' interface.
    ###########################################################################
    
    def initialize(self, preferences, path=None):
        """ Initialize the object from a preference node. """

        if path is None:
            path = self.path

        # fixme: The 'path' trait is in the namespace....
        for trait_name in self.trait_names():
            # Ignore private/protected traits.
            if trait_name.startswith('_'):
                continue

            # Ignore traits traits!
            if trait_name.startswith('trait_'):
                continue

            value = preferences.get('%s.%s' % (path, trait_name), Undefined)
            if value is not Undefined:
                setattr(self, trait_name, value)

        return
        
#### EOF ######################################################################
