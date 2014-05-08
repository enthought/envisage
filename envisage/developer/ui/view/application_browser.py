""" A view showing a summary of the running application. """


# Standard library imports.
import inspect

# Enthought library imports.
from envisage.api import IApplication, IPlugin
from envisage.developer.code_browser.api import CodeBrowser
from apptools.io.api import File
from traits.api import Any, HasTraits, Instance
from traitsui.api import Item, TreeEditor, View

# fixme: non-api import.
from envisage.plugins.text_editor.editor.text_editor import TextEditor

# Local imports.
from .application_browser_tree import application_browser_tree_nodes


application_browser_view = View(
    Item(
        name       = 'application',
        show_label = False,
        editor     = TreeEditor(
            nodes       = application_browser_tree_nodes,
            editable    = False,
            orientation = 'vertical',
            hide_root   = True,
            show_icons  = True,
            selected    = 'selection',
            on_dclick   = 'object.dclick'
        )
    ),

    resizable = True,
    style     = 'custom',
    title     = 'Application',

    width     = .1,
    height    = .1
)


class ApplicationBrowser(HasTraits):
    """ An application browser.

    Actually, this class exists just because to use a trait editor we have
    to have a trait to edit!

    """

    # The application that we are browsing.
    application = Instance(IApplication)

    # The code browser that we use to parse plugin source code.
    code_browser = Instance(CodeBrowser)

    # The workbench service.
    workbench = Instance('envisage.ui.workbench.api.Workbench')

    # The object that is currently selected in the tree.
    selection = Any

    # The default traits UI view.
    traits_view = application_browser_view

    ###########################################################################
    # 'ApplicationBrowser' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _code_browser_default(self):
        """ Trait initializer. """

        return self.application.get_service(CodeBrowser)

    def _workbench_default(self):
        """ Trait initializer. """

        from envisage.ui.workbench.api import Workbench

        return self.application.get_service(Workbench)

    #### Trait change handlers ################################################

    def _selection_changed(self, trait_name, old, new):
        """ Static trait change handler. """

        #print 'Selection changed', trait_name, old, new

        return

    #### Methods ##############################################################

    def dclick(self, obj):
        """ Called when an object in the tree is double-clicked. """

        if IPlugin(obj, None) is not None:
            # Parse the plugin source code.
            module = self._parse_plugin(obj)

            # Get the plugin klass.
            klass = self._get_plugin_klass(module, obj)

            # Edit the plugin.
            editor = self.workbench.edit(
                self._get_file_object(obj), kind=TextEditor
            )

            # Move to the class definition.
            editor.select_line(klass.lineno)

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_file_object(self, obj):
        """ Return a 'File' object for an object's source file. """

        return File(path=inspect.getsourcefile(type(obj)))

    def _get_plugin_klass(self, module, plugin):
        """ Get the klass that defines the plugin. """

        for name, klass in module.klasses.items():
            if name == type(plugin).__name__:
                break

        else:
            klass = None

        return klass

    def _parse_plugin(self, plugin):
        """ Parse the plugin source code. """

        filename = self._get_file_object(plugin).path

        return self.code_browser.read_file(filename)

#### EOF ######################################################################
