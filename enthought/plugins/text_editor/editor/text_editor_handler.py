""" The traits UI handler for the text editor.

fixme: This is currently set up for Python files, but should work for any text
file.  We need to generalize this code to support all text editing.

"""


# Enthought library imports.
from enthought.traits.ui.api import CodeEditor, Group, Handler, Item, View
from enthought.traits.ui.key_bindings import KeyBinding, KeyBindings
from enthought.traits.ui.menu import NoButtons


# fixme: Key bindings need to be set dynamically when the editor is created.
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


class TextEditorHandler(Handler):
    """ The traits UI handler for the text editor. """

    #### 'TextEditor' interface ###############################################

    # The default traits view.
    traits_view = View(
        Group(
            Item('text', editor=CodeEditor(key_bindings=key_bindings)),
            show_labels = False
        ),
        
        buttons   = NoButtons,
        height    = 1.0,
        id        = 'enthought.envisage.editor.text_editor',
        kind      = 'live',
        resizable = True,
        width     = 1.0,
    )    

    ###########################################################################
    # 'TextEditor' interface.
    ###########################################################################

    def run(self, info):
        """ Runs the text as Python code. """

        obj = info.ui.context['object']
        obj.run()

        return
    
    def save(self, info):
        """ Saves the text to disk. """

        obj = info.ui.context['object']
        obj.save()

        return

#### EOF ######################################################################
