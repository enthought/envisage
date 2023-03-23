# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Run the MOTD example application. """

# Enthought library imports.
from envisage.api import Application, CorePlugin


def main():
    """Run the application."""
    # Import here so that this script can be run from anywhere without
    # having to install the packages.
    from acme.motd.motd_plugin import MOTDPlugin
    from acme.motd.software_quotes.software_quotes_plugin import (
        SoftwareQuotesPlugin,
    )

    # Create an application containing the appropriate plugins.
    application = Application(
        id="acme.motd",
        plugins=[CorePlugin(), MOTDPlugin(), SoftwareQuotesPlugin()],
    )

    # Run it!
    return application.run()


if __name__ == "__main__":
    # This context manager is added so that one can run this example from any
    # directory without necessarily having installed the examples as packages.
    from envisage.examples._demo import demo_path

    with demo_path(__file__):
        main()
