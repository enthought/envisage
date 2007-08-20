""" The default preference scope. """


# Local imports.
from preferences import Preferences


class DefaultPreferences(Preferences):
    """ The default preference scope. """

    ###########################################################################
    # 'Preferences' interface.
    ###########################################################################

    def save(self, filename=None):
        """ Save the node to a 'ConfigObj' file. """

        # We don't want to save the defaults!
        pass
    
#### EOF ######################################################################




