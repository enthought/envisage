# Enthought library imports.
from traits.api import HasTraits, Str, Unicode


class PreferencesCategory(HasTraits):
    """ The description for a container of PreferencesPanes.
    """

    # The globally unique identifier for the category.
    id = Str

    # The user-visible name of the category.
    name = Unicode

    # The category appears after the category with this ID.
    before = Str

    # The category appears after the category with this ID.
    after = Str

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _name_default(self):
        """ By default, use the ID for the name.
        """
        return self.id
