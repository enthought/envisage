# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
"""
The single project plugin's project view

"""

# Standard library imports.
import logging

# Enthought library imports
from apptools.naming.api import Binding
from traits.api import register_factory, Any, HasTraits, Instance, Str
from traitsui.api import Item, Group, TreeEditor, ITreeNode, \
    ITreeNodeAdapter, View

# Application specific imports.
from envisage.api import IApplication
from envisage.ui.single_project.project import Project
from envisage.ui.single_project.services import IPROJECT_MODEL, \
    IPROJECT_UI


# Setup a logger for this module.
logger=logging.getLogger(__name__)


# Dummy EmptyProject class for when the ProjectView doesn't have a reference
# to a Project.
class EmptyProject(Project):
    pass

class EmptyProjectAdapter(ITreeNodeAdapter):
    """ Adapter for our EmptyProject. """

    #-- ITreeNodeAdapter Method Overrides --------------------------------------

    def get_label(self):
        """ Gets the label to display for a specified object.
        """
        return 'No project loaded.'

register_factory(EmptyProjectAdapter, EmptyProject, ITreeNode)


class ProjectAdapter(ITreeNodeAdapter):
    """ Base ProjectAdapter for the root of the tree. """

    #-- ITreeNodeAdapter Method Overrides --------------------------------------

    def allows_children(self):
        """ Returns whether this object can have children.
        """
        return False

    def has_children(self):
        """ Returns whether the object has children.
        """
        return False

    def get_children(self):
        """ Gets the object's children.
        """
        return []

    def get_label(self):
        """ Gets the label to display for a specified object.
        """
        return self.adaptee.name

    def get_tooltip(self):
        """ Gets the tooltip to display for a specified object.
        """
        return "Project"

    def get_icon(self, is_expanded):
        """ Returns the icon for a specified object.
        """
        return '<open>'

    def can_auto_close(self):
        """ Returns whether the object's children should be automatically
            closed.
        """
        return True

register_factory(ProjectAdapter, Project, ITreeNode)


class ProjectView(HasTraits):
    """
    The single project plugin's project view

    """

    ##########################################################################
    # Traits
    ##########################################################################

    #### public 'ProjectView' interface ######################################

    # The Envisage application that this service is part of.
    application = Instance(IApplication)

    # The suffix currently applied to our name
    name_suffix = Str('')

    # The suffix applied to titles when the current project is dirty.
    title_suffix = Str('*')

    # Root node for the project.
    root = Instance(Project)

    # The traits view to display:
    view = View(
        Item('root', editor = TreeEditor(editable=False, auto_open=1),
            show_label = False,
        ),
        resizable = True
    )

    ##########################################################################
    # 'View' interface.
    ##########################################################################
    def __init__(self, **traits):
        super(ProjectView, self).__init__(**traits)

        # Make sure our view stays in sync with the current project
        model_service = self._get_model_service()
        model_service.on_trait_change(self._on_project_changed, 'project')
        model_service.on_trait_change(self._on_project_selection_changed,
            'selection')

        # Make sure our control is initialized to the current project.
        self._switch_projects(EmptyProject(), model_service.project)

    ##########################################################################
    # 'ProjectView' interface.
    ##########################################################################

    #### protected 'ProjectView' interface #################################

    def _are_list_contents_different(self, list1, list2):
        """
        Convenience method to determine if two lists contain different
        items.  Returns True if the lists are different and False
        otherwise.

        """
        set1 = set(list1)
        set2 = set(list2)
        return set1 != set2


    def _clear_state(self):
        """
        Clears out all indications of any project state from this view.

        """

        #self.name_suffix = ''
        # Set the root to an EmptyProject.
        self.root = EmptyProject()

        return


    def _get_model_service(self):
        """
        Return a reference to the single project plugin's model service.

        """

        return self.application.get_service(IPROJECT_MODEL)


    def _get_ui_service(self):
        """
        Return a reference to the single project plugin's UI service.

        """

        return self.window.application.get_service(IPROJECT_UI)


    def _switch_projects(self, old, new):
        """
        Switches this view to the specified new project from the old project.

        Either value may be None.

        """

        # Remove listeners on the old project, if any.
        if old is not None and not isinstance(old, EmptyProject):
            self._update_project_listeners(old, remove=True)

        # Update our state according to what the new project is, making sure
        # to add listeners to any new project.
        if new is not None:
            logger.debug("Changing ProjectView to Project [%s]", new.name)
            self._sync_state_to_project(new)
            self._update_project_listeners(new)
        else:
            logger.debug("Changing ProjectView to no project")
            self._clear_state()

        return


    def _sync_state_to_project(self, project):
        """
        Sync the state of this view to the specified project's state.

        """

        logger.debug('Syncing ProjectView [%s] to project state [%s]', self,
            project)

        # Update our Project reference.
        self.root = project

        # Update our name suffix based on the dirty state of the project.
        #self.name_suffix = (project.dirty and self.title_suffix) or ''

        return


    def _update_project_listeners(self, project, remove=False):
        """
        Update listeners on the specified project instance.

        If remove is False then listeners are added, else listeners
        are removed.

        """

        project.on_trait_change(self._on_project_name_changed, 'name', remove)
        project.on_trait_change(self._on_project_dirty_changed, 'dirty',
            remove)

        return


    #### trait handlers ######################################################

    def _name_suffix_changed(self, old, new):
        """
        Handle changes to our name suffix.

        """

        logger.debug('Detected change in name suffix to [%s] within ' + \
            'ProjectView [%s]', new, self)

        # Update our own name by removing the old suffix, if any, and adding
        # on the new suffix, if any.
        name = self.name
        if old is not None and len(old) > 0:
            index = (" " + old).rfind(name)
            if index > -1:
                name = name[0:index]
        if new is not None and len(new) > 0:
            name = name + ' ' + new
        self.name = name

        # Update the containing window's suffix as well
        self.window.title_suffix = new

        return


    def _on_control_right_clicked (self, event):
        """
        Handle events when the tree control itself is right-clicked.

        """

        logger.debug('ProjectView control right-clicked')
        self._get_ui_service().display_default_context_menu(self.control, event)

        return


    def _on_key_pressed_changed(self, event):
        """
        Handle key presses while our control has focus.

        """

        logger.debug("ProjectView key pressed [%s]", event)

        # If the delete key was pressed, then delete the current selected
        # object.
        if event.key_code == 127:
            self._get_ui_service().delete_selection()

        return


    def _on_node_activated_changed(self, node):
        """
        Handle nodes being activated (i.e. double-clicked.)

        """

        logger.debug("ProjectView node activated [%s]", node)

        return


    def _on_project_changed(self, obj, trait_name, old, new):
        """
        Handle when the current project changes.

        """

        logger.debug('\n\n ***************** \n\n')
        logger.debug('Detected project changed from [%s] to [%s] in '
            'ProjectView [%s]', old, new, self)

        self._switch_projects(old, new)

        return


    def _on_project_dirty_changed(self, obj, trait_name, old, new):
        """
        Handle the open project's dirty flag changing.

        """

        logger.debug('Detected change in project dirty to [%s] within ' + \
            'ProjectView [%s]', new, self)

        suffix = (new and self.title_suffix) or ''
        #self.name_suffix = suffix

        return


    def _on_project_name_changed(self, obj, trait_name, old, new):
        """
        Handle the open project's name changing.

        """

        self._project_control.root.name = new

        return


    def _on_project_selection_changed(self, obj, trait_name, old, new):
        """
        Handle the current project's selection changing.

        """

        logger.debug('Detected project selection changed from [%s] ' + \
            'to [%s] within ProjectView [%s]', old, new, self)

        # Ensure that the Tree control's selection matches the selection in
        # the project.
        control_selection = self._project_control.selection
        if self._are_list_contents_different(new, control_selection):
            logger.debug('  Updating selection on tree control for ' + \
                'ProjectView [%s]', self)
            self._project_control.set_selection(new)

        # Ensure that this view's selection contains whatever was selected
        # within the project.
        if self._are_list_contents_different(new, self.selection):
            logger.debug('  Updating selection on ProjectView [%s]', self)
            self.selection = new

        return


    def _on_selection_changed(self, obj, trait_name, old, new):
        """
        Handle selection changes in our tree control.

        """

        logger.debug('Detected tree control selection change from [%s] ' + \
            'to [%s] within ProjectView [%s]', old, new, self)

        # Ensure that the project model service's record of selection contains
        # the same elements as the tree control.
        model_service = self._get_model_service()
        if self._are_list_contents_different(new, model_service.selection):
            logger.debug('  Updating selection on project model service')
            model_service.selection = new

        # Note that we don't have to update this view's selection record as
        # we do that through our listener on the project selection.

        return


    def _on_closing_changed(self, old, new):
        """
        Handle when this view closes.

        """

        logger.debug("ProjectView [%s] closing!", self)

        return


#### EOF #####################################################################
