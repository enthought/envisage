""" A view showing a summary of the running application. """


# Standard library imports.
import inspect

# Enthought library imports.
from enthought.envisage.api import IApplication, IPlugin, Service
from enthought.io.api import File
from enthought.traits.api import Any, HasTraits, Instance
from enthought.traits.ui.api import Item, View

# fixme: non-api import.
from enthought.plugins.text_editor.editor.text_editor import TextEditor

# Local imports.
from application_browser_tree_editor import application_browser_tree_editor


application_view = View(
    Item(
        name       = 'application',
        show_label = False,
        editor     = application_browser_tree_editor
    ),

    resizable = True,
    style     = 'custom',
    title     = 'Application',

    width     = .2,
    height    = .4
)


class ApplicationBrowser(HasTraits):
    """ An application browser.

    Actually, this class exists just because to use a trait editor we have
    to have a trait to edit!

    """

    # The application that we are browsing.
    application = Instance(IApplication)

    # The workbench service.
    workbench = Service('enthought.envisage.ui.workbench.api.Workbench')
    
    # The object that is currently selected in the tree.
    selection = Any
    
    # The default traits UI view.
    traits_view = application_view

    ###########################################################################
    # 'ApplicationBrowser' interface.
    ###########################################################################

    #### Trait change handlers ################################################

    def _selection_changed(self, trait_name, old, new):
        """ Static trait change handler. """

        print 'Selection changed', trait_name, old, new

        return

    #### Methods ##############################################################
    
    def dclick(self, obj):
        """ Called when an object in the tree is double-clicked. """

        if IPlugin(obj, None) is not None:
            self.workbench.edit(self._get_file_object(obj), kind=TextEditor)
            
        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_file_object(self, obj):
        """ Return a 'File' object for the object's source file. """
        
        return File(path=inspect.getsourcefile(type(obj)))
    
#### EOF ######################################################################
