""" Run the MOTD example application. """


# Enthought library imports.
from envisage.api import Application, CorePlugin

# Example plugins.
from acme.motd.motd_plugin import MOTDPlugin
from acme.motd.software_quotes.software_quotes_plugin import (
    SoftwareQuotesPlugin,
)


def main():
    """ Run the application. """

    # Create an application containing the appropriate plugins.
    application = Application(
        id="acme.motd",
        plugins=[CorePlugin(), MOTDPlugin(), SoftwareQuotesPlugin()],
    )

    # Run it!
    return application.run()


if __name__ == "__main__":
    main()
