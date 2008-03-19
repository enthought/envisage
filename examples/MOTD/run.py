""" Run the MOTD example application. """


# Standard library imports.
import logging



# Enthought library imports.
from enthought.envisage.api import Application

# Do whatever you want to do with log messages! Here we create a log file.
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(file('acme_motd.log', 'w')))
logger.setLevel(logging.DEBUG)

# Enthought plugins.
from enthought.envisage.core_plugin import CorePlugin

# Example plugins.
from acme.motd.motd_plugin import MOTDPlugin
from acme.motd.software_quotes.software_quotes_plugin import SoftwareQuotesPlugin




def main():
    """ Run the application. """


    # Create an application that uses the egg plugin manager to find its
    # plugins.
    application = Application(
        id      = 'acme.motd',
        plugins = [CorePlugin(), MOTDPlugin(), SoftwareQuotesPlugin()]
    )

    # Run it!
    return application.run()


if __name__ == '__main__':
    main()

#### EOF ######################################################################
