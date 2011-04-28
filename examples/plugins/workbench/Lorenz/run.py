""" Run the Lorenz example application. """


# Standard library imports.
import logging

# Enthought plugins.
from envisage.core_plugin import CorePlugin
from envisage.ui.workbench.workbench_plugin import WorkbenchPlugin

# Example imports.
from acme.lorenz.lorenz_application import LorenzApplication
from acme.lorenz.lorenz_plugin import LorenzPlugin
from acme.lorenz.lorenz_ui_plugin import LorenzUIPlugin


# Do whatever you want to do with log messages! Here we create a log file.
logger = logging.getLogger()
#logger.addHandler(logging.StreamHandler(file('lorenz.log', 'w')))
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def main():
    """ Run the application. """

    # Create an application with the specified plugins.
    lorenz_application = LorenzApplication(
        plugins=[
            CorePlugin(), WorkbenchPlugin(), LorenzPlugin(), LorenzUIPlugin()
        ]
    )

    # Run it! This starts the application, starts the GUI event loop, and when
    # that terminates, stops the application.
    lorenz_application.run()

    return


if __name__ == '__main__':
    main()

#### EOF ######################################################################
