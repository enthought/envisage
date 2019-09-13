# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" An action that saves the current project. """

# Enthought library imports.
from envisage.ui.single_project.project_action import ProjectAction
from pyface.api import ImageResource

##############################################################################
# class 'SaveProjectAction'
##############################################################################

class SaveProjectAction(ProjectAction):
    """ An action that saves the current project. """

    # The universal object locator (UOL).
    uol = 'envisage.ui.single_project.ui_service.UiService'

    # The name of the method to invoke on the object.
    method_name = 'save'

    # A longer description of the action.
    description = 'Save the current project'

    # The action's image (displayed on tool bar tools etc).
    image = ImageResource('save_project')

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'Save'

    # A short description of the action used for tooltip text etc.
    tooltip = 'Save this project'

    #### public interface ####################################################

    def refresh(self):
        """
        Refresh the enabled state of this action.

        This implementation enables the action when there is a current project
        which is marked as saveable.

        """

        self.enabled = self._refresh_project_exists() and \
            self._refresh_is_save_allowed()

        return


    #### trait handlers ######################################################

    def _on_project_changed(self, obj, trait_name, old, new):
        """
        Handle changes to the value of the current project.

        Extended to ensure that we listen for changes to the saveable flag on
        the current project.

        """

        if old is not None:
            self._update_project_listeners(old, remove=True)
        if new is not None:
            self._update_project_listeners(new, remove=False)

        super(SaveAction, self)._on_project_changed(obj, trait_name, old, new)


    ##########################################################################
    # 'SaveAction' interface
    ##########################################################################

    #### protected interface #################################################

    def _refresh_is_save_allowed(self):
        """
        Return the refresh state according to whether the current project is
        marked as saveable.

        Returns True if the action should be enabled and False otherwise.

        """

        return self.model_service.project.is_save_allowed


    def _update_project_listeners(self, project, remove):
        """
        Update listeners on the specified project.

        """

        logger.debug( (remove and 'Removing ' or 'Adding ') + \
            'listeners on project [%s] for SaveAction [%s]', project, self)

        project.on_trait_change(self._on_is_save_allowed, 'is_save_allowed',
            remove=remove)

        return


    #### trait handlers ######################################################

    def _on_is_save_allowed(self, obj, trait_name, old, new):
        """
        Handle changes to the value of the current project's is_save_allowed.

        """

        self.refresh()

        return
