""" The entry point for the MOTD application. """


# Enthought library imports.
from enthought.envisage.api import ConsoleApplication


def run():
    """ Run the application. """

    return ConsoleApplication(id='acme.motd').run()


if __name__ == '__main__':
    run()
    
#### EOF ######################################################################
