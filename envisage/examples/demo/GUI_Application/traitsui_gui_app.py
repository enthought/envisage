# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A simple example of a GUIApplication which wraps a TraitsUI """

from pyface.api import SplashScreen
from traits.api import Enum, HasTraits, Instance, Int, on_trait_change, Str
from traitsui.api import Item, View

from envisage.api import CorePlugin, Plugin
from envisage.ui.api import GUIApplication, GUIPlugin


class Person(HasTraits):
    """A typical traits model object"""

    name = Str("John Doe")

    age = Int(21)

    gender = Enum("Male", "Female")

    view = View(
        Item("name"),
        Item("age"),
        Item("gender"),
    )


class PersonViewPlugin(Plugin):
    """The 'Person View' plugin.

    This plugin waits for the application to start, and then creates a traits
    UI.

    """

    ui = Instance("traitsui.ui.UI")

    @on_trait_change("application:application_initialized")
    def on_application_start(self):
        """Start the UI."""

        person = Person()

        # keep a reference to the ui object to avoid garbage collection
        self.ui = person.edit_traits(kind="live")


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
        splash_screen=SplashScreen(image="splash"),
    )

    # Run it!
    application.run()


# Application entry point.
if __name__ == "__main__":
    main()
