""" An editor manager that uses contributed editors. """

# Enthought library imports.
from pyface.workbench.api import EditorManager, TraitsUIEditor


class WorkbenchEditorManager(EditorManager):
    """ An editor manager that uses contributed editors. """

    ###########################################################################
    # 'IEditorManager' interface.
    ###########################################################################

    def create_editor(self, window, obj, kind):
        """ Create an editor for an object.

        For now, the 'kind' is actually a factory that produces editors. It
        should be a callable with the following signature::

            callable(window=window, obj=obj) -> IEditor
        """

        if kind is None:
            kind = TraitsUIEditor

        editor = kind(window=window, obj=obj)

        self.add_editor(editor, kind)

        return editor

    ###########################################################################
    # 'Protected' 'EditorManager'  interface.
    ###########################################################################

    def _is_editing(self, editor, obj, kind):
        """ Return True if the editor is editing the object. """

        if kind is None:
            kind = TraitsUIEditor
        return self.get_editor_kind(editor) is kind and editor.obj == obj

#### EOF ######################################################################
