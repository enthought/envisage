""" A view containing the contents of a Python shell namespace. """

# Enthought library imports.
from enthought.plugins.python_shell.api import IPythonShell
from enthought.plugins.ipython_shell.api import INamespaceView
from enthought.pyface.workbench.api import View
from enthought.traits.api import Property, implements, Instance
from enthought.traits.ui.api import Item, TreeEditor
from enthought.traits.ui.api import View as TraitsView
from enthought.traits.ui.value_tree import RootNode, value_tree_nodes
from enthought.pyface.timer.api import Timer
from enthought.pyface.api import GUI

class NamespaceView(View):
    """ A view containing the contents of the Python shell namespace. """

    implements(INamespaceView)

    #### 'IView' interface ####################################################

    # The part's globally unique identifier.
    id = 'Enthoughtght.plugins.ipython_shell.namespace_view'

    # The view's name.
    name = 'Namespace'

    # The default position of the view relative to the item specified in the
    # 'relative_to' trait.
    position = 'left'

    #### 'NamespaceView' interface ############################################

    # The different tree nodes
    tree_nodes = Property

    # The default traits UI view.
    traits_view = TraitsView(
            Item(
                'tree_nodes',
                id     = 'table',
                editor = TreeEditor( 
                                auto_open=1,
                                hide_root=True,
                                editable=False,
                                nodes=value_tree_nodes,
                                ),
                springy = True,
                resizable = True,
                show_label = False
            ),
            resizable = True,
        )

    # The timer used to refresh the ui
    _refresh_tree_nodes_timer = Instance(Timer)

    def __refresh_tree_nodes_timer_default(self):
        return Timer(100, self._refresh_tree_nodes)

    ###########################################################################
    # 'View' interface.
    ###########################################################################

    def create_control(self, parent):
        """ Creates the toolkit-specific control that represents the view.

        'parent' is the toolkit-specific control that is the view's parent.

        """

        self.ui = self.edit_traits(parent=parent, kind='subpanel')

        # Register the view as a service.
        self.window.application.register_service(INamespaceView, self)

        shell = self.window.application.get_service(IPythonShell)
        if shell is not None:
            shell.on_trait_change(self._on_names_changed, 'names')
            self._on_names_changed(shell.names)

        return self.ui.control


    def destroy_control(self):
        """ Destroys the toolkit-specific control that represents the view.

        """
        
        super(NamespaceView, self).destroy_control()

        # Remove the namespace change handler
        shell= self.window.application.get_service(IPythonShell)
        if shell is not None:
            shell.on_trait_change(
                self._on_names_changed, 'names', remove=True
            )


    ###########################################################################
    # 'NamespaceView' interface.
    ###########################################################################

    #### Properties ###########################################################

    def _get_tree_nodes(self):
        """ Property getter. """
        
        shell = self.window.application.get_service(IPythonShell)

        # Cater for an un-initialized python shell view
        if shell is None:
            return RootNode(name='<empty namespace>', value=[],
                            readonly=True)
        filtered_namespace = dict()
        for name in shell.names:
            filtered_namespace[name] = shell.lookup(name)

        return RootNode(name='', value=filtered_namespace,
                            readonly=True).tno_get_children(None)[0]

    

    def _refresh_tree_nodes(self):
        """ Callback called by a timer to refresh the UI.

            The UI is refreshed by a timer to buffer the refreshes,
            in order not to slow down the execution engine.
        """
        self.trait_property_changed('tree_nodes', [], self.tree_nodes)
        self._refresh_tree_nodes_timer.Stop()

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handlers ################################################
    
    def _on_names_changed(self, new):
        """ Dynamic trait change handler. """

        # fixme: We might want to get a tad more granular in the event that we
        # fire!
        if not self._refresh_tree_nodes_timer.IsRunning():
            GUI.invoke_later(self._refresh_tree_nodes_timer.Start)

    
#### EOF ######################################################################
