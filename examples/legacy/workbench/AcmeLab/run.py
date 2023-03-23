# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Run the AcmeLab example application. """


# Standard library imports.
import logging

# Example imports.
from acme.acmelab.api import Acmelab

# Enthought plugins.
from envisage.api import CorePlugin
from envisage.ui.workbench.workbench_plugin import WorkbenchPlugin

# Example plugins.
from acme.workbench.acme_workbench_plugin import AcmeWorkbenchPlugin


# Do whatever you want to do with log messages! Here we create a log file.
logger = logging.getLogger()
# logger.addHandler(logging.StreamHandler(file('acmelab.log', 'w')))
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def main():
    """ Run the application. """

    # Create an application with the specified plugins.
    acmelab = Acmelab(
        plugins=[CorePlugin(), WorkbenchPlugin(), AcmeWorkbenchPlugin()]
    )

    # Run it! This starts the application, starts the GUI event loop, and when
    # that terminates, stops the application.
    acmelab.run()

    return


if __name__ == "__main__":
    main()
