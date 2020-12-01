# Plugin imports.
from envisage.api import CorePlugin
from envisage.ui.tasks.api import TasksPlugin


def main(argv):
    """ Run the application.
    """
    # Import here so that this script can be run from anywhere without
    # having to install the packages.
    from attractors.attractors_plugin import AttractorsPlugin
    from attractors.attractors_application import AttractorsApplication

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
