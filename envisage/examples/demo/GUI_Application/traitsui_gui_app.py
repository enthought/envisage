""" A simple example of a GUIApplication which wraps a TraitsUI """

from traits.api import HasTraits, Str, Int, Enum, Instance, on_trait_change
from envisage.api import Plugin
from envisage.ui.gui_application import GUIApplication
from traitsui.api import View, Item, OKCancelButtons


class Person(HasTraits):
    """ A typical traits model object """

    name = Str("John Doe")

    age = Int(21)

    gender = Enum("Male", "Female")

    view = View(
        Item("name"), Item("age"), Item("gender"), buttons=OKCancelButtons,
    )


class PersonViewPlugin(Plugin):
    """ The 'Person View' plugin.

    This plugin waits for the application to start, and then creates a traits
    UI.

    """

    ui = Instance("traitsui.ui.UI")

    @on_trait_change("application:application_initialized")
    def on_application_start(self):
        """ Start the UI. """

        person = Person()

        # keep a reference to the ui object to avoid garbage collection
        self.ui = person.edit_traits()


# Application entry point.
if __name__ == "__main__":

    # Create the application.
    application = GUIApplication(
        id="person_view", plugins=[PersonViewPlugin()]
    )

    # Run it!
    application.run()
