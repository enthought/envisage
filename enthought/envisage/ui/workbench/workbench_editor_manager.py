""" An editor manager that uses contributed editors. """


# Standard library imports.
import weakref

# Enthought library imports.
from enthought.pyface.workbench.api import EditorManager, TraitsUIEditor


class WorkbenchEditorManager(EditorManager):
    """ An editor manager that uses contributed editors. """

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Constructor. """

        super(WorkbenchEditorManager, self).__init__(**traits)

        # A mapping from editor to editor kind (the factory that created them).
        self._editor_to_kind_map = weakref.WeakKeyDictionary()

        return
    
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

        # Save the factory that created the editor so that we can allow the
        # same object to be edited by different editors in the same window.
        self._editor_to_kind_map[editor] = kind
        
        return editor

    ###########################################################################
    # 'Protected' 'EditorManager'  interface.
    ###########################################################################

    def _is_editing(self, editor, obj, kind):
        """ Return True if the editor is editing the object. """

        if kind is None:
            kind = TraitsUIEditor
        return self._editor_to_kind_map[editor] is kind and editor.obj == obj

#### EOF ######################################################################
