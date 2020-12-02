""" Run the MOTD example application. """

# Enthought library imports.
from envisage.api import Application, CorePlugin


def main():
    """ Run the application. """
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
