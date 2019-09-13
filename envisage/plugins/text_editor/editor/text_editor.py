# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" A text editor. """


# Standard library imports.
from os.path import basename

# Enthought library imports.
from pyface.workbench.api import TraitsUIEditor
from pyface.api import FileDialog, CANCEL
from traits.api import Code, Instance
from traitsui.api import CodeEditor, Group, Item, View
from traitsui.key_bindings import KeyBinding, KeyBindings
from traitsui.menu import NoButtons

# Local imports.
from .text_editor_handler import TextEditorHandler


def _id_generator():
    """ A generator that returns the next number for untitled files. """

    i = 1
    while True:
        yield(i)
        i += 1

    return

_id_generator = _id_generator()


class TextEditor(TraitsUIEditor):
    """ A text editor. """

    #### 'TextEditor' interface ###############################################

    # The key bindings used by the editor.
    key_bindings = Instance(KeyBindings)

    # The text being edited.
    text = Code

    ###########################################################################
    # 'IEditor' interface.
    ###########################################################################

    def save(self):
        """ Saves the text to disk. """

        # If the file has not yet been saved then prompt for the file name.
        if len(self.obj.path) == 0:
            self.save_as()

        else:
            f = open(self.obj.path, 'w')
            f.write(self.text)
            f.close()

            # We have just saved the file so we ain't dirty no more!
            self.dirty = False

        return

    def save_as(self):
        """ Saves the text to disk after prompting for the file name. """

        dialog = FileDialog(
            parent           = self.window.control,
            action           = 'save as',
            default_filename = self.name,
            wildcard         = FileDialog.WILDCARD_PY
        )
        if dialog.open() != CANCEL:
            # Update the editor.
            self.id   = dialog.path
            self.name = basename(dialog.path)

            # Update the resource.
            self.obj.path = dialog.path

            # Save it!
            self.save()

        return

    ###########################################################################
    # 'TraitsUIEditor' interface.
    ###########################################################################

    def create_ui(self, parent):
        """ Creates the traits UI that represents the editor. """

        ui = self.edit_traits(
            parent=parent, view=self._create_traits_ui_view(), kind='subpanel'
        )

        return ui

    ###########################################################################
    # 'TextEditor' interface.
    ###########################################################################

    def run(self):
        """ Runs the file as Python. """

        # The file must be saved first!
        self.save()

        # Execute the code.
        if len(self.obj.path) > 0:
            view = self.window.get_view_by_id(
                'envisage.plugins.python_shell_view'
            )

            if view is not None:
                view.execute_command(
                    'exec(open(r"%s").read())' % self.obj.path, hidden=False
                )

        return

    def select_line(self, lineno):
        """ Selects the specified line. """

        self.ui.info.text.selected_line = lineno

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _key_bindings_default(self):
        """ Trait initializer. """

        key_bindings = KeyBindings(
            KeyBinding(
                binding1    = 'Ctrl-s',
                description = 'Save the file',
                method_name = 'save'
            ),

            KeyBinding(
                binding1    = 'Ctrl-r',
                description = 'Run the file',
                method_name = 'run'
            )
        )

        return key_bindings

    #### Trait change handlers ################################################

    def _obj_changed(self, new):
        """ Static trait change handler. """

        # The path will be the empty string if we are editing a file that has
        # not yet been saved.
        if len(new.path) == 0:
            self.id   = self._get_unique_id()
            self.name = self.id

        else:
            self.id   = new.path
            self.name = basename(new.path)

            f = open(new.path, 'r')
            self.text = f.read()
            f.close()

        return

    def _text_changed(self, trait_name, old, new):
        """ Static trait change handler. """

        if self.traits_inited():
            self.dirty = True

        return

    def _dirty_changed(self, dirty):
        """ Static trait change handler. """

        if len(self.obj.path) > 0:
            if dirty:
                self.name = basename(self.obj.path) + '*'

            else:
                self.name = basename(self.obj.path)

        return

    #### Methods ##############################################################

    def _create_traits_ui_view(self):
        """ Create the traits UI view used by the editor.

        fixme: We create the view dynamically to allow the key bindings to be
        created dynamically (we don't use this just yet, but obviously plugins
        need to be able to contribute new bindings).

        """

        view = View(
            Group(
                Item(
                    'text', editor=CodeEditor(key_bindings=self.key_bindings)
                ),
                show_labels = False
            ),

            id        = 'envisage.editor.text_editor',
            handler   = TextEditorHandler(),
            kind      = 'live',
            resizable = True,
            width     = 1.0,
            height    = 1.0,
            buttons   = NoButtons,
        )

        return view

    def _get_unique_id(self, prefix='Untitled '):
        """ Return a unique id for a new file. """

        id = prefix + str(next(_id_generator))
        while self.window.get_editor_by_id(id) is not None:
            id = prefix + str(next(_id_generator))

        return id

#### EOF ######################################################################
