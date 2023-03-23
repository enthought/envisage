# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The Envisage version of the old chestnut. """

from traits.api import List, Str

# Enthought library imports.
from envisage.api import Application, ExtensionPoint, Plugin


class HelloWorld(Plugin):
    """The 'Hello World' plugin.

    This plugin offers a single extension point 'greetings' which is a list of
    greetings, one of which is used to produce the '<greeting> World' message
    when the plugin is started.

    """

    # This tells us that the plugin offers the 'greetings' extension point,
    # and that plugins that want to contribute to it must each provide a list
    # of strings (Str).
    greetings = ExtensionPoint(
        List(Str), id="greetings", desc='Greetings for "Hello World"'
    )

    # Plugin's have two important lifecyle methods, 'start' and 'stop'. These
    # methods are called automatically by Envisage when the application is
    # started and stopped respectively.
    def start(self):
        """Start the plugin."""

        # Standard library imports.
        #
        # We put this import here just to emphasize that it is only used in
        # this specific plugin.
        import random

        print("{} World!".format(random.choice(self.greetings)))


class Greetings(Plugin):
    """A plugin that contributes to the 'greetings' extension point."""

    # This tells us that the plugin contributes the value of this trait to the
    # 'greetings' extension point.
    greetings = List(["Hello", "G'day"], contributes_to="greetings")


class MoreGreetings(Plugin):
    """Another plugin that contributes to the 'greetings' extension point."""

    # This tells us that the plugin contributes the value of this trait to the
    # 'greetings' extension point.
    greetings = List(contributes_to="greetings")

    # This shows how you can use a standard trait initializer to populate the
    # list dynamically.
    def _greetings_default(self):
        """Trait initializer."""

        extensions = [
            "The %s application says %s" % (self.application.id, greeting)
            for greeting in ["Bonjour", "Hola"]
        ]

        return extensions


# Application entry point.
if __name__ == "__main__":
    # Create the application.
    #
    # An application is simply a collection of plugins. In this case we
    # specify the plugins explicitly, but the mechanism for finding plugins
    # is configurable by setting the application's 'plugin_manager' trait.
    application = Application(
        id="hello.world", plugins=[HelloWorld(), Greetings(), MoreGreetings()]
    )

    # Run it!
    application.run()
