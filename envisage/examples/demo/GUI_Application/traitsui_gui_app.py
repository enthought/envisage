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

from traits.api import Enum, HasTraits, Instance, Int, on_trait_change, Str
from traitsui.api import Item, OKCancelButtons, View

from envisage.api import Plugin
from envisage.ui.gui_application import GUIApplication


class Person(HasTraits):
    """A typical traits model object"""

    name = Str("John Doe")

    age = Int(21)

    gender = Enum("Male", "Female")

    view = View(
        Item("name"),
        Item("age"),
        Item("gender"),
        buttons=OKCancelButtons,
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
        self.ui = person.edit_traits()


# Application entry point.
if __name__ == "__main__":
    # Create the application.
    application = GUIApplication(
        id="person_view", plugins=[PersonViewPlugin()]
    )

    # Run it!
    application.run()
