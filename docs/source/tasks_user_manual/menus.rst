.. _menus:

====================
 Menus and Tool Bars
====================

In addition to specifying a layout of panes, a task can include a menu bar, a
status bar, and any number of tool bars. In this section, we shall see how the
Tasks framework supports these important user interface elements.

It is important to recall that a task is a kind of *blueprint* for a user
interface. As such, a task can provide blueprints, or *schemas* as we shall
henceforth call them, for menus and tool bars, but does not itself contain menu
or tool bar controls. This distinction, though perhaps not very useful in the
present section, will take on considerable importance in the subsequent section
on :ref:`extensibility`.

.. index:: menu bar

Defining a Menu Bar
-------------------

.. index:: Action

Resuming our example of the script editing task from the previous section, we
shall define some menu items for opening and saving files. As in Traits UI and
PyFace, individual menu items are instances of the ``Action`` class [1]_. We
might define the 'Open' action as follows::

    from pyface.action.api import Action

    class OpenAction(Action):
        name = 'Open'
        accelerator = 'Ctrl+O'

        def perform(self, event):
            event.task.open()

Of course, we must also implement the ``open()`` method on our task::

    from pyface.api import FileDialog, OK

    class ExampleTask(Task):
    
        [ ... ]

        def open(self):
            """ Shows a dialog to open a file.
            """
            dialog = FileDialog(parent=self.window.control, wildcard='*.py')
            if dialog.open() == OK:
                # Recall that 'open_file' was defined in the previous section.
                self.open_file(dialog.path)

.. index:: MenuBarSchema, MenuSchema, GroupSchema, SMenuBar, SMenu, SGroup

Now let us suppose that we have similarly implemented a ``SaveAction`` and a
``save()`` method on our task. We would like to add these actions to a menu
bar. Tasks provides several ``Schema`` classes for this purpose:

:``MenuBarSchema``: The root of a menu hierarchy. Contains some number of menu
                    schemas.
:``MenuSchema``:    A menu or sub-menu in the menu hierarchy.
:``GroupSchema``:   A group of menu items that are logically related and that 
                    may or may not require separators from other groups.

For convenience, these classes also have the abbreviated names ``SMenuBar``,
``SMenu``, and ``SGroup``, respectively. We can implement the menu bar for our
task using these abbreviations::

    from pyface.tasks.action.api import SMenu, SMenuBar

    class ExampleTask(Task):

        [ ... ]

        menu_bar = SMenuBar(SMenu(OpenAction(), SaveAction(),
                                  id='File', name='&File'))

.. index:: TaskAction

The pattern of having an ``Action`` instance call back to its task is so common
that there is a predefined class for this purpose. We can use this
``TaskAction`` class to implement the above menu more simply, without having to
define separately the ``OpenAction`` and ``SaveAction`` classes::

    from pyface.tasks.action.api import SMenu, SMenuBar, TaskAction

    class ExampleTask(Task):

        [ ... ]

        menu_bar = SMenuBar(SMenu(TaskAction(name='Open...', method='open',
                                             accelerator='Ctrl+O'),
                                  TaskAction(name='Save', method='save',
                                             accelerator='Ctrl+S'),
                                  id='File', name='&File'))

.. index:: tool bar

Defining a Tool Bar
-------------------

.. index:: ToolBarSchema, SToolBar

Like a menu bar, a tool bar uses the ``Action`` class to represent individual
items. A tool bar, however, is defined with a different set of schemas:

:``ToolBarSchema``: The root of a tool bar hierarchy. Contains some number of 
                    group schemas and actions.
:``GroupSchema``:   A group of tool bar buttons that are logically related and
                    that may or may not require separators from other groups.

As above, these classes are often abbreviated as ``SToolBar`` and ``SGroup``,
respectively. Let us now add a tool bar with buttons for opening and saving
files to our script editing task::

    from pyface.api import ImageResource
    from pyface.tasks.action.api import SToolBar, TaskAction

    class ExampleTask(Task):
        
        [ ... ]

        tool_bars = [ SToolBar(TaskAction(method='open',
                                          tooltip='Open a file',
                                          image=ImageResource('document_open')),
                               TaskAction(method='save',
                                          tooltip='Save the current file',
                                          image=ImageResource('document_save'))) ]

.. rubric:: Footnotes

.. [1] The most convenient reference in this case is the `source code
       <https://github.com/enthought/traitsgui/blob/master/enthought/pyface/action/action.py>`_ itself.

