# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
import logging

from apptools.io.api import File
from pyface.api import FileDialog, OK
from pyface.action.api import Action
from traits.api import Any

from .editor.text_editor import TextEditor

logger = logging.getLogger(__name__)

class NewFileAction(Action):
    """ Open a new file in the text editor.
    """
    tooltip = "Create a new file for editing"
    description = "Create a new file for editing"

    # The WorkbenchWindow the action is attached to.
    window = Any()

    def perform(self, event=None):
        logger.info('NewFileAction.perform()')
        self.window.workbench.edit(File(''), kind=TextEditor,
            use_existing=False)


class OpenFileAction(Action):
    """ Open an existing file in the text editor.
    """
    tooltip = "Open a file for editing"
    description = "Open a file for editing"

    def perform(self, event=None):
        logger.info('OpenFileAction.perform()')
        dialog = FileDialog(parent=self.window.control,
            title='Open File')
        if dialog.open() == OK:
            self.window.workbench.edit(File(dialog.path), kind=TextEditor)

