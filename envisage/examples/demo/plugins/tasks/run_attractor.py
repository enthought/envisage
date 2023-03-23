# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

# Plugin imports.
from envisage.api import CorePlugin
from envisage.ui.tasks.api import TasksPlugin


def main(argv):
    """Run the application."""
    # Import here so that this script can be run from anywhere without
    # having to install the packages.
    from attractors.attractors_application import AttractorsApplication
    from attractors.attractors_plugin import AttractorsPlugin

    plugins = [CorePlugin(), TasksPlugin(), AttractorsPlugin()]
    app = AttractorsApplication(plugins=plugins)
    app.run()


if __name__ == "__main__":
    import sys

    # This context manager is added so that one can run this example from any
    # directory without necessarily having installed the examples as packages.
    from envisage.examples._demo import demo_path

    with demo_path(__file__):
        main(sys.argv)
