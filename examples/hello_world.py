""" The Envisage version of the old chestnut. """


# Enthought library imports.
from enthought.envisage.api import Application, ExtensionPoint, Plugin
from enthought.traits.api import List, Str


class HelloWorld(Plugin):
    """ A plugin that offers an extension point. """

    # This tells us that this plugin offers the 'greetings' extension point,
    # and that each plugin that wants to contribute to it must provide a list
    # of strings (Str).
    greetings = ExtensionPoint(
        List(Str), id='greetings', desc='Greetings for "Hello World"'
    )

    # Plugin's have two important lifecyle methods, 'start' and 'stop'.
    # These methods can be called manually, but usually they are called when
    # the application is started and stopped respectively.
    def start(self):
        """ Start the plugin. """

        # Standard library imports.
        import random

        print random.choice(self.greetings), 'World!'
        
        return


class Greetings(Plugin):
    """ A plugin that contributes to the extension point. """

    # This tells us that the plugin contributes to the 'greetings' extension
    # point using this trait.
    greetings = List(["Hello", "G'day"], extension_point='greetings')


class MoreGreetings(Plugin):
    """ Another plugin that contributes to the extension point. """

    # This tells us that the plugin contributes to the 'greetings' extension
    # point using this trait.
    greetings = List(['Bonjour', 'Ola'], extension_point='greetings')


# Application entry point.
if __name__ == '__main__':
    
    # Create the application.
    application = Application(
        id='hello.world', plugins=[HelloWorld(), Greetings(), MoreGreetings()]
    )

    # Run it!
    application.run()

#### EOF ######################################################################
