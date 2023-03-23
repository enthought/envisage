# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The Envisage workbench. """


# Enthought library imports.
import pyface.workbench.api as pyface
from pyface.api import YES
from traits.api import Delegate, Instance

from envisage.api import IApplication

# Local imports.
from .workbench_preferences import WorkbenchPreferences
from .workbench_window import WorkbenchWindow


class Workbench(pyface.Workbench):
    """The Envisage workbench.

    There is (usually) exactly *one* workbench per application. The workbench
    can create any number of workbench windows.

    """

    #### 'pyface.Workbench' interface #########################################

    # The factory that is used to create workbench windows.
    window_factory = WorkbenchWindow

    #### 'Workbench' interface ################################################

    # The application that the workbench is part of.
    application = Instance(IApplication)

    # Should the user be prompted before exiting the workbench?
    prompt_on_exit = Delegate("_preferences")

    #### Private interface ####################################################

    # The workbench preferences.
    _preferences = Instance(WorkbenchPreferences, ())

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _exiting_changed(self, event):
        """Called when the workbench is exiting."""

        if self.prompt_on_exit:
            answer = self.active_window.confirm(
                "Exit %s?" % self.active_window.title, "Confirm Exit"
            )
            if answer != YES:
                event.veto = True
