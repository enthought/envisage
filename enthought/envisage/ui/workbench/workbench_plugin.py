""" The Envisage workbench plugin. """


# Enthought library imports.
from enthought.envisage.api import ExtensionPoint, Plugin
from enthought.traits.api import Callable, List, Instance


class WorkbenchPlugin(Plugin):
    """ The Envisage workbench plugin.

    The workbench plugin uses the PyFace workbench to provide the basis of an
    IDE-like user interface. The interface is made of up perspectives, views
    and editors.

    Note that this is not intended to be a 'general-purpose' plugin for user
    interfaces - it provides an IDE-like style and that is all. If your
    application requires another style of interface then write another plugin
    (you can still re-use all the menu, group and action contribution stuff!).

    """

    # Extension point Ids.
    ACTIONS           = 'enthought.envisage.ui.workbench.actions'
    PERSPECTIVES      = 'enthought.envisage.ui.workbench.perspectives'
    PREFERENCES_PAGES = 'enthought.envisage.ui.workbench.preferences_pages'
    VIEWS             = 'enthought.envisage.ui.workbench.views'
    
    #### 'IPlugin' interface ##################################################

    id   = 'enthought.envisage.ui.workbench'
    name = 'Workbench'

    #### 'WorkbenchPlugin' interface ##########################################

    ###########################################################################
    # Extension points offered by this plugin.
    ###########################################################################
    
    actions = ExtensionPoint(
        List(Instance('enthought.envisage.ui.action.api.IActionSet')),
        id   = ACTIONS,
        desc = """

        This extension point allows you to contribute menus, groups and actions
        to the workbench menu and tool bars. You can create new menus and
        groups or add to existing ones.

        """
    )
    
    perspectives = ExtensionPoint(
        List(Instance('enthought.envisage.ui.workbench.api.IPerspective')),
        id   = PERSPECTIVES,
        desc = """

        This extension point allows you to contribute perspectives to the
        workbench. Each perspective is just an arrangement of views around an
        (optional) editor area.

        """
    )

    preferences_pages = ExtensionPoint(
        List(Instance('enthought.preferences.ui.api.IPreferencesPage')),
        id   = PREFERENCES_PAGES,
        desc = """

        This extension points allows you to contribute pages to the
        preferences dialog.

        """
    )
    
    views = ExtensionPoint(
        List(Callable),
        id   = VIEWS,
        desc = """

        This extension point allows you to contribute views to the workbench.
        Each extension must be a callable with the following signature::

          callable(**traits) -> IView

        i.e. It should be a callable that takes keyword arguments that specify
        the view's traits, and should return an object that implements the
        'IView' interface. A class that implements 'IView' would do nicely ;^)
         
        """
    )

    ###########################################################################
    # Contributions to extension points made by this plugin.
    ###########################################################################

    workbench_actions           = List(extension_point=ACTIONS)
    workbench_preferences_pages = List(extension_point=PREFERENCES_PAGES)

    ###########################################################################
    # Services offered by this plugin.
    ###########################################################################

    workbench = Instance(
        'enthought.envisage.ui.workbench.api.Workbench', service=True
    )
        
    ###########################################################################
    # 'WorkbenchPlugin' interface.
    ###########################################################################

    #### Extension point contributions ########################################
    
    def _workbench_actions_default(self):
        """ Trait initializer. """

        from default_action_set import DefaultActionSet

        return [DefaultActionSet()]

    def _workbench_preferences_pages_default(self):
        """ Trait initializer. """
        
        from workbench_preferences_page import WorkbenchPreferencesPage
        
        return [WorkbenchPreferencesPage()]

    #### Services #############################################################

    def _workbench_default(self):
        """ Trait initializer. """

        # fixme: This guard is really just for testing when we have the
        # workbench plugin as a source egg (i.e. if the egg is on our path
        # then we get the plugin for any egg-based application, even if it is
        # not a workbench application!).
        return getattr(self.application, 'workbench', None)

### EOF ######################################################################
