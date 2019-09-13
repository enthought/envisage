# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" A view containing the contents of a Python shell namespace. """

import types

# Enthought library imports.

from envisage.plugins.python_shell.api import IPythonShell
from envisage.plugins.python_shell.view.python_shell_view import PythonShellView

from pyface.workbench.api import View

from traits.api import HasTraits, Str, Property, List, Instance, \
        DelegatesTo, cached_property

from traitsui.api import Item, TableEditor, VGroup
from traitsui.api import View as TraitsView
from traitsui.table_column import ObjectColumn
from traitsui.table_filter import RuleTableFilter
from traitsui.table_filter import MenuFilterTemplate
from traitsui.table_filter import EvalFilterTemplate
from traitsui.table_filter import RuleFilterTemplate


# Table editor definition:
filters = [EvalFilterTemplate, MenuFilterTemplate, RuleFilterTemplate]

table_editor = TableEditor(
    columns     = [
        ObjectColumn(name='name'),
        ObjectColumn(name='type'),
        ObjectColumn(name='module'),
    ],
    editable    = False,
    deletable   = False,
    sortable    = True,
    sort_model  = False,
    filters     = filters,
    search      = RuleTableFilter(),
)


def type_to_str(obj):
    """
    Make a string out `obj`'s type robustly.
    """
    typ = type(obj)
    if typ.__name__ == 'vtkobject' or typ is types.InstanceType:
        typ = obj.__class__
    if type.__module__ == '__builtin__':
        # Make things like int and str easier to read.
        return typ.__name__
    else:
        name = '%s.%s' % (typ.__module__, typ.__name__)
        return name


def module_to_str(obj):
    """
    Return the string representation of *obj*'s ``__module__`` attribute, or
    an empty string if there is no such attribute.
    """
    if hasattr(obj, '__module__'):
        return str(obj.__module__)
    else:
        return ''


class NamespaceView(View):
    """ A view containing the contents of the Python shell namespace. """

    #### 'IView' interface ####################################################

    # The part's globally unique identifier.
    id = 'enthought.plugins.python_shell.view.namespace_view'

    # The view's name.
    name = 'Namespace'

    # The default position of the view relative to the item specified in the
    # 'relative_to' trait.
    position = 'left'

    #### 'NamespaceView' interface ############################################

    # The bindings in the namespace.  This is a list of HasTraits objects with
    # 'name', 'type' and 'module' string attributes.
    bindings = Property(List, depends_on=['namespace'])

    shell_view = Instance(PythonShellView)

    namespace = DelegatesTo('shell_view')


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

        self.shell_view = self.window.application.get_service(IPythonShell)
        # 'shell_view' is an instance of the class PythonShellView from the module
        # envisage.plugins.python_shell.view.python_shell_view.

        return self.ui.control

    ###########################################################################
    # 'NamespaceView' interface.
    ###########################################################################

    #### Properties ###########################################################

    @cached_property
    def _get_bindings(self):
        """ Property getter. """

        if self.shell_view is None:
            return []

        class item(HasTraits):
            name = Str
            type = Str
            module = Str

        data = [item(name=name, type=type_to_str(value), module=module_to_str(value))
                    for name, value in self.shell_view.namespace.items()]

        return data
