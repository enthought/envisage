""" An action that configures an item in the project tree. """

# Enthought library imports.
from envisage.ui.single_project.project_action import ProjectAction

##############################################################################
# class 'ConfigureAction'
##############################################################################

class ConfigureAction(ProjectAction):
    """ An action that configures an item in the project tree.

    'Configures' in this sense means pop up a trait sheet!

    """

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Performs the action. """

        # fixme: We would like to use "kind='modal'" here, but it doesn't
        # work! The bug we see is that when the dialog is complete the
        # viscosity model assigned to the trait is NOT the same as the
        # viscosity model in the material's '_dirty_objects' collection!
        ui = event.node.obj.edit_traits(
            parent=event.window.control, kind='livemodal'
        )

        return

#### EOF ######################################################################
