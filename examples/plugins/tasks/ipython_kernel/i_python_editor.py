""" A widget for editing Python code. """


# Enthought library imports.
from traits.api import Bool, Event, Instance, File, Unicode
from pyface.tasks.i_editor import IEditor

# Local imports.
from pyface.key_pressed_event import KeyPressedEvent


class IPythonEditor(IEditor):
    """ A widget for editing Python code. """

    #### 'IPythonEditor' interface ############################################

    # Object being editor is a file
    obj = Instance(File)

    # The pathname of the file being edited.
    path = Unicode

    # Should line numbers be shown in the margin?
    show_line_numbers = Bool(True)

    #### Events ####

    # The contents of the editor has changed.
    changed = Event

    # A key has been pressed.
    key_pressed = Event(KeyPressedEvent)

    ###########################################################################
    # 'IPythonEditor' interface.
    ###########################################################################

    def load(self, path=None):
        """ Loads the contents of the editor. """

    def save(self, path=None):
        """ Saves the contents of the editor. """

    def select_line(self, lineno):
        """ Selects the specified line. """
