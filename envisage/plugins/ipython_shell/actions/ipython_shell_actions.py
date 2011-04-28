from envisage.ui.action.api import Action, ActionSet, Group
from pyface.action.api import Action as PyfaceAction
from envisage.plugins.python_shell.api import IPythonShell


def get_shell(window):
    """ Given an application window, retrieve the ipython shell.
    """
    return window.application.get_service(IPythonShell)

################################################################################
# Groups
################################################################################
ipython_shell_group = Group(
    id='IPythonShellGroup',
    path='MenuBar/Tools',
    #before='ExitGroup'
)


################################################################################
# `ClearScreen` class.
################################################################################
class ClearScreen(PyfaceAction):
    """ An action that clears the IPython screen. """

    tooltip      = "Clear the IPython screen."

    description  = "Clear the IPython screen."


    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Performs the action. """
        shell = get_shell(self.window)

        if shell is not None:
            shell.control.clear_screen()

clear_screen = Action(
    path        = "MenuBar/Tools",
    class_name  = __name__ + '.ClearScreen',
    name        = "Clear IPython screen",
    group       = "IPythonShellGroup",
)


################################################################################
# `IPythonShellActionSet` class.
################################################################################
class IPythonShellActionSet(ActionSet):
    """ The default action set for the IPython shell plugin. """

    groups = [ipython_shell_group, ]

    actions = [clear_screen]
