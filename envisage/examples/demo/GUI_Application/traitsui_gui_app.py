""" A simple example of a GUIApplication which wraps a TraitsUI """

from envisage.api import CorePlugin, Plugin
from envisage.ui.api import GUIApplication, GUIPlugin
from pyface.api import SplashScreen
from traits.api import HasTraits, Str, Int, Enum, Instance, on_trait_change
from traitsui.api import View, Item


class Person(HasTraits):
    """ A typical traits model object """

    name = Str("John Doe")

    age = Int(21)

    gender = Enum("Male", "Female")

    view = View(
        Item("name"),
        Item("age"),
        Item("gender"),
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
        self.ui = person.edit_traits(kind='live')


def main():
    """Main method of the traitsui gui app example"""

    # Create the application.
    application = GUIApplication(
        id="person_view",
        plugins=[
            CorePlugin(),
            GUIPlugin(),
            PersonViewPlugin(),
        ],
        splash_screen=SplashScreen(image='splash'),
    )

    # Run it!
    application.run()


# Application entry point.
if __name__ == "__main__":
    main()
