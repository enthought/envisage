# Standard library imports.
import logging

# Plugin imports.
from envisage.core_plugin import CorePlugin
from envisage.ui.tasks.tasks_plugin import TasksPlugin
from attractors_plugin import AttractorsPlugin

# Local imports.
from attractors_application import AttractorsApplication


def main(argv):
    """ Run the application.
    """
    logging.basicConfig(level=logging.WARNING)

    plugins = [ CorePlugin(), TasksPlugin(), AttractorsPlugin() ]
    app = AttractorsApplication(plugins=plugins)
    app.run()

    logging.shutdown()


if __name__ == '__main__':
    import sys
    main(sys.argv)
