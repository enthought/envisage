""" An editor manager that uses contributed editors. """


# Enthought library imports.
from enthought.pyface.workbench.api import EditorManager, TraitsUIEditor


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

        #print 'WorkbenchEditorManager.create_editor', obj, kind
        
        if kind is None:
            kind = TraitsUIEditor
            
        return kind(window=window, obj=obj)

##     def get_editor_memento(self, editor):
##         """ Return the state of an editor suitable for pickling etc.

##         By default we don't save the state of editors.

##         """

##         return None

##     def set_editor_memento(self, memento):
##         """ Restore the state of an editor from a memento.

##         By default we don't try to restore the state of editors.

##         """

##         return None

#### EOF ######################################################################
