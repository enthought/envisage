""" A text editor. """


# Standard library imports.
from os.path import basename

# Enthought library imports.
from enthought.pyface.workbench.api import TraitsUIEditor
from enthought.pyface.api import FileDialog, CANCEL
from enthought.traits.api import Code, Instance

# Local imports.
from text_editor_handler import TextEditorHandler


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
            f = file(self.obj.path, 'w')
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

        ui = TextEditorHandler().edit_traits(
            context=self, parent=parent, kind='panel'
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
                'enthought.plugins.python_shell.view.PythonShellView'
            )

            if view is not None:
                view.execute_command(
                    'execfile(r"%s")' % self.obj.path, hidden=False
                )
            
        return
    
    def select_line(self, lineno):
        """ Selects the specified line. """

        self.ui.info.text.selected_line = lineno

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Methods ##############################################################
    
    def _get_unique_id(self, prefix='Untitled '):
        """ Returns a unique id for a new file. """

        id = prefix + str(_id_generator.next())
        while self.window.get_editor_by_id(id) is not None:
            id = prefix + str(_id_generator.next())

        return id
    
    #### Trait change handlers ################################################

    #### Static ####
    
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

            f = file(new.path, 'r')
            self.text = f.read()
            f.close()
        
        return

    #### Dynamic ####
    
    def _on_dirty_changed(self, dirty):
        """ Dynamic trait change handler. """

        if len(self.obj.path) > 0:
            if dirty:
                self.name = basename(self.obj.path) + '*'
                
            else:
                self.name = basename(self.obj.path)
            
        return
    
#### EOF ######################################################################
