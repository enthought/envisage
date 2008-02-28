""" Run the AcmeLab example application. """


# Standard library imports.
import logging

# Enthought library imports.
from enthought.envisage.api import EggPluginManager

# Example imports.
from acme.acmelab.api import Acmelab


# Enthought plugins.
from enthought.envisage.core_plugin import CorePlugin
from enthought.envisage.ui.workbench.workbench_plugin import WorkbenchPlugin

# Example plugins.
from acme.workbench.workbench_plugin import WorkbenchPlugin as AcmeWorkbenchPlugin


# Create a log file.
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(file('acmelab.log', 'w')))
#logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def main():
    """ Run the application. """


    # Create an application that uses the egg plugin manager to find its
    # plugins.
    acmelab = Acmelab(
        plugins = [
            CorePlugin(),
            WorkbenchPlugin(),
            AcmeWorkbenchPlugin()
        ]
    )

    # Run it! This starts the application, starts the GUI event loop, and when
    # that terminates, stops the application.
    acmelab.run()


if __name__ == '__main__':
    main()

#### EOF ######################################################################
