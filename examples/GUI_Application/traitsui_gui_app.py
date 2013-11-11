""" A simple example of a GUIApplication which wraps a TraitsUI """

from traits.api import HasTraits, Str, Int, Enum, Instance
from envisage.api import Plugin
from envisage.ui.gui_application import GUIApplication
from traitsui.api import View, Item, OKCancelButtons

class Person(HasTraits):
    """ A typical traits model object """
    
    name = Str("John Doe")
    
    age = Int(21)
    
    gender = Enum("Male", "Female")

    view = View(
        Item('name'),
        Item('age'),
        Item('gender'),
        buttons = OKCancelButtons,
    )

class PersonViewPlugin(Plugin):
    """ The 'Person View' plugin.

    When started, this plugin creates a Person instance, and opens an
    editor for it.  When the application shuts down, it checks whether
    the user cancelled or 

    """
    
    ui = Instance('traitsui.ui.UI')

    def start(self):
        """ Start the plugin. """
        
        person = Person()
        
        # keep a reference to the ui object to avoid garbage collection
        self.ui = person.edit_traits()
        
        return True
    
    def stop(self):
        if self.ui.result:
            print "User OK"
        else:
            print "User Cancel"

# Application entry point.
if __name__ == '__main__':

    # Create the application.
    #
    # An application is simply a collection of plugins. In this case we
    # specify the plugins explicitly, but the mechanism for finding plugins
    # is configurable by setting the application's 'plugin_manager' trait.
    application = GUIApplication(
        id='person_view', plugins=[PersonViewPlugin()]
    )

    # Run it!
    application.run()
