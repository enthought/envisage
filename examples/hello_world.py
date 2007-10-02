""" The Envisage version of the old chestnut. """


# Standard library imports.
import random

# Enthought library imports.
from enthought.envisage.api import Application, ExtensionPoint, Plugin
from enthought.traits.api import List, Str


class HelloWorld(Plugin):
    """ A plugin that offers an extension point. """
    
    greetings = ExtensionPoint(List(Str), id='greetings')

    def start(self):
        """ Start the plugin. """
                
        print random.choice(self.greetings), 'World!'
        
        return


class Greetings(Plugin):
    """ A plugin that contributes to the extension point. """
    
    greetings = List(["Hello", "G'day"], extension_point='greetings')


class MoreGreetings(Plugin):
    """ A plugin that contributes to the extension point. """

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
