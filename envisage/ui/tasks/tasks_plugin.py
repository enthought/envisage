# Enthought library imports.
from envisage.api import ExtensionPoint, Plugin, ServiceOffer
from traits.api import Callable, List

# Local imports.
from .preferences_category import PreferencesCategory
from .task_factory import TaskFactory
from .task_extension import TaskExtension

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

    # The IDs of the extension points that this plugin contributes to.
    SERVICE_OFFERS = 'envisage.service_offers'

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'envisage.ui.tasks'

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
        that derives from 'envisage.ui.tasks.api.PreferencesPane'.
        """)

    tasks = ExtensionPoint(
        List(TaskFactory), id=TASKS, desc="""

        This extension point makes tasks avaiable to the application.

        Each contribution to the extension point must be an instance of
        'envisage.tasks.api.TaskFactory.
        """)

    task_extensions = ExtensionPoint(
        List(TaskExtension), id=TASK_EXTENSIONS, desc="""

        This extension point permits the contribution of new actions and panes
        to existing tasks (without creating a new task).

        Each contribution to the extension point must be an instance of
        'envisage.tasks.api.TaskExtension'.
        """)

    #### Contributions to extension points made by this plugin ################

    my_service_offers = List(contributes_to=SERVICE_OFFERS)

    def _my_service_offers_default(self):
        preferences_dialog_service_offer = ServiceOffer(
            protocol = 'envisage.ui.tasks.preferences_dialog.'
                       'PreferencesDialog',
            factory  = self._create_preferences_dialog_service)

        return [ preferences_dialog_service_offer ]

    my_task_extensions = List(contributes_to=TASK_EXTENSIONS)

    def _my_task_extensions_default(self):
        from .action.exit_action import ExitAction
        from .action.preferences_action import PreferencesGroup
        from pyface.tasks.action.api import DockPaneToggleGroup, \
             SchemaAddition

        actions = [ SchemaAddition(id='Exit',
                                   factory=ExitAction,
                                   path='MenuBar/File'),
                    SchemaAddition(id='Preferences',
                                   factory=PreferencesGroup,
                                   path='MenuBar/Edit'),
                    SchemaAddition(id='DockPaneToggleGroup',
                                   factory=DockPaneToggleGroup,
                                   path='MenuBar/View') ]

        return [ TaskExtension(actions=actions) ]

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_preferences_dialog_service(self):
        """ Factory method for preferences dialog service.
        """
        from .preferences_dialog import PreferencesDialog

        dialog = PreferencesDialog(application = self.application)
        dialog.trait_set(categories = self.preferences_categories,
                         panes = [ factory(dialog = dialog)
                                   for factory in self.preferences_panes ])
        return dialog
