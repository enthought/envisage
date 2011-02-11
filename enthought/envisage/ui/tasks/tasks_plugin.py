# Enthought library imports.
from enthought.envisage.api import ExtensionPoint, Plugin, ServiceOffer
from enthought.traits.api import Callable, List

# Local imports.
from preferences_category import PreferencesCategory
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
    PREFERENCES_CATEGORIES = PKG + '.preferences_categories'
    PREFERENCES_PANES      = PKG + '.preferences_panes'
    TASKS                  = PKG + '.tasks'
    TASK_EXTENSIONS        = PKG + '.task_extensions'

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'enthought.envisage.ui.tasks'

    # The plugin's name (suitable for displaying to the user).
    name = 'Tasks'

    #### Extension points offered by this plugin ##############################

    preferences_categories = ExtensionPoint(
        List(PreferencesCategory), id=PREFERENCES_CATEGORIES, desc="""

        This extension point makes preference categories available to the
        application. Note that preference categories will be created
        automatically if necessary; this extension point is useful when one
        wants to ensure that a category is inserted at a specific location.

        """)

    preferences_panes = ExtensionPoint(
        List(Callable), id=PREFERENCES_PANES, desc="""

        A preferences pane appears in the preferences dialog to allow the user 
        manipulate certain preference values.

        Each contribution to this extension point must be a factory that
        creates a preferences pane, where 'factory' means any callable with the
        following signature::

          callable(**traits) -> PreferencesPane

        The easiest way to contribute such a factory is to create a class
        that derives from 'enthought.envisage.ui.tasks.api.PreferencesPane'.
        """)

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
