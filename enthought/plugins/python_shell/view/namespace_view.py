""" A view containing the contents of a Python shell namespace. """


# Enthought library imports.
from enthought.plugins.python_shell.api import IPythonShell
from enthought.pyface.workbench.api import View
from enthought.traits.api import HasTraits, Str, Property
from enthought.traits.ui.api import Item, TableEditor, VGroup
from enthought.traits.ui.api import View as TraitsView
from enthought.traits.ui.table_column import ListColumn, ObjectColumn
from enthought.traits.ui.table_filter import RuleTableFilter
from enthought.traits.ui.table_filter import MenuFilterTemplate
from enthought.traits.ui.table_filter import EvalFilterTemplate
from enthought.traits.ui.table_filter import RuleFilterTemplate


# Table editor definition:  
filters = [EvalFilterTemplate, MenuFilterTemplate, RuleFilterTemplate]

table_editor = TableEditor(
    columns     = [
        ObjectColumn(name='name'),
        ObjectColumn(name='type')
    ],
    editable    = False,
    deletable   = False,
    sortable    = True,
    sort_model  = False,
    filters     = filters,
    search      = RuleTableFilter(),
)

    
class NamespaceView(View):
    """ A view containing the contents of the Python shell namespace. """

    #### 'IView' interface ####################################################

    # The view's name.
    name = 'Namespace'

    # The default position of the view relative to the item specified in the
    # 'relative_to' trait.
    position = 'left'

    #### 'NamespaceView' interface ############################################

    # The bindings in the namespace.
    bindings = Property

    # The default traits UI view.
    traits_view = TraitsView(
        VGroup(
            Item(
                'bindings',
                id     = 'table',
                editor = table_editor,
                springy = True,
                resizable = True,
            ),

            show_border = True,
            show_labels = False
        ),
        resizable = True,
    )

    ###########################################################################
    # 'View' interface.
    ###########################################################################

    def create_control(self, parent):
        """ Creates the toolkit-specific control that represents the view.

        'parent' is the toolkit-specific control that is the view's parent.

        """

        self.ui = self.edit_traits(parent=parent, kind='subpanel')

        shell = self.window.application.get_service(IPythonShell)
        shell.on_trait_change(self._on_names_changed, 'names')
        
        return self.ui.control

    ###########################################################################
    # 'NamespaceView' interface.
    ###########################################################################

    #### Properties ###########################################################

    def _get_bindings(self):
        """ Property getter. """
        
        shell = self.window.application.get_service(IPythonShell)

        # fixme: We should be able to use a list of lists instead of having
        # to create these objects!
        class item(HasTraits):
            name = Str
            type = Str

        data = [
            item(name=name, type=str(type(shell.lookup(name))))
            for name in shell.names
        ]

        return data
    
    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handlers ################################################
    
    def _on_names_changed(self, new):
        """ Dynamic trait change handler. """

        # fixme: We might want to get a tad more granular in the event that we
        # fire!
        self.trait_property_changed('bindings', [], self.bindings)
        
        return
    
#### EOF ######################################################################
