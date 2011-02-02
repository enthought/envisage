# Enthought library imports.
from enthought.envisage.api import ExtensionPoint, Plugin, ServiceOffer
from enthought.traits.api import Callable, List

# Local imports.
from task_factory import TaskFactory
from task_extension import TaskExtension

# Constants.
PKG = '.'.join(__name__.split('.')[:-1])


class TasksPlugin(Plugin):
    """ The Envisage Tasks plugin.

    The Tasks plugin uses PyFace Tasks to provide an extensible framework for
    building user interfaces. For more information, see the Tasks User Manual.
    """

    # The IDs of the extension point that this plugin offers.
    TASKS           = PKG + '.tasks'
    TASK_EXTENSIONS = PKG + '.task_extensions'

    # THE IDs of extension points that this plugin contributes to.
    SERVICE_OFFERS = 'enthought.envisage.service_offers'

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'enthought.envisage.ui.tasks'

    # The plugin's name (suitable for displaying to the user).
    name = 'Tasks'

    #### Extension points offered by this plugin ##############################

    tasks = ExtensionPoint(
        List(TaskFactory), id=TASKS, desc="""

        This extension point makes tasks avaiable to the application.

        Each contribution to the extension point must be an instance of
        'enthought.envisage.tasks.api.TaskFactory.
        """)

    task_extensions = ExtensionPoint(
        List(TaskExtension), id=TASK_EXTENSIONS, desc="""

        This extension point permits the contribution of new actions and panes
        to existing tasks (without creating a new task).

        Each contribution to the extension point must be an instance of
        'enthought.envisage.tasks.api.TaskExtension'.
        """)
