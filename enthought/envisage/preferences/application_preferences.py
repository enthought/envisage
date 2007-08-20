""" The application preference scope. """


# Standard library imports.
import os

# Enthought library imports.
from enthought.etsconfig.api import ETSConfig
from enthought.traits.api import Str

# Local imports.
from preferences import Preferences


class ApplicationPreferences(Preferences):
    """ The application preference scope. """

    #### 'ApplicationPreferences' interface ###################################

    # The name of the file used to persist the preferences.
    filename = Str

    ###########################################################################

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Constructor. """

        super(ApplicationPreferences, self).__init__(**traits)

        # Load the scope at startup.
        self.load(self.filename)

        print 'foogle', self.get('martin.foogle', 'Nah!!!!!!!!!!!!')
        
        return
    
    ###########################################################################
    # Application'Preferences' interface.
    ###########################################################################

    def _filename_default(self):
        """ Trait initializer. """

        return os.path.join(ETSConfig.application_home, 'preferences.ini')
        
    ###########################################################################
    # 'Preferences' interface.
    ###########################################################################

    def save(self, filename=None):
        """ Save the node to a 'ConfigObj' file. """

        if filename is None:
            filename = self.filename
            
        super(ApplicationPreferences, self).save(filename)

        return

    ###########################################################################
    # Protected 'Preferences' interface.
    ###########################################################################

    # We have to override this method, otherwise we create more application
    # preferences which will try to load themselves ad nauseum!
    def _create_child(self, name):
        """ Create a child node with the specified name. """

        child = Preferences(name=name, parent=self)
        self.children[name] = child

        return child

#### EOF ######################################################################




