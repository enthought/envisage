.. _layout:

=======================
 Window Layout
=======================

First and foremost, the Tasks plugin is designed to facilitate the layout of
modern, customizable user interfaces. Accordingly, we shall begin by learning
how to use Tasks to perform basic window layout.

.. index:: task; lifecycle

Lifecycle of a Task
-------------------

.. index:: model-view-controller pattern, MVC

The Tasks plugin adheres to the model-view-controller (MVC) design pattern [1]_,
for which the ``Task`` class functions as the controller and the ``TaskWindow``
class as the view, with the model being application-specific [2]_. Insofar as a
``Task`` is a controller, it does not itself instantiate or contain any GUI
controls, although it does provide factories and a default layout for the
controls that it manages. Controls are instantiated when a ``Task`` is assigned
to a ``TaskWindow``. Specifically, the following actions are taken at this time:

1. The task's central pane is constructed and attached to the window
2. All of the task's dock panes are constructed, even if they are not by default
   visible
3. The visible dock panes are laid out around the central pane according to the
   task's default layout or persisted UI state information

While the ``Task`` remains connected to the ``TaskWindow``, neither its central
pane nor its dock panes will be destroyed. If the user "closes" a dock pane, the
pane will be merely hidden, and can be re-activated via the application's View
menu. Only when the ``Task`` itself is closed---that is, when it is removed from
the ``TaskWindow``---will its panes be destroyed. This marks the end of the
``Task``'s lifecycle. If the task is to be re-used, a new instance should be
constructed.

.. index:: task; defining

Defining a Task
---------------

Minimally, a task is defined by subclassing ``Task`` and providing a central
pane. For example, we define a task for editing Python scripts [3]_::

    from pyface.tasks.api import Task

    class ExampleTask(Task):

        id = 'example.example_task'
        name = 'Python Script Editor'

        def create_central_pane(self):
            return PythonEditorPane()

.. index:: ID, name

The ``id`` attribute is a unique internal identifier for the task, whereas
``name`` is a user-visible descriptor for the task. We shall see that this is a
common pattern in the Tasks framework.

.. index:: central pane; defining

All tasks must implement ``create_central_pane()`` and return a TaskPane
instance. We might define the ``PythonEditorPane`` pane above as follows, making
use of the ``PythonEditor`` available in PyFace::

    from pyface.api import PythonEditor
    from pyface.tasks.api import TaskPane
    from traits.api import Instance

    class PythonEditorPane(TaskPane):

        id = 'example.python_editor_pane'
        name = 'Python Editor'

        editor = Instance(PythonEditor)

        def create(self, parent):
            self.editor = PythonEditor(parent)
            self.control = self.editor.control

        def destroy(self):
            self.editor.destroy()
            self.control = self.editor = None

Besides providing an ID and a name for the pane, we implement the two basic
methods of ``TaskPane``, namely ``create(parent)`` and ``destroy()``. The former
constructs a toolkit-specific control for the pane and assigns its to the pane's
``control`` attribute. The latter performs the inverse operation, destroying the
control and clearing ``control`` attribute. These methods give one full control
over how a pane is constructed, but as we shall see below there are other, more
convenient methods for defining a pane.

.. index:: dock pane; defining

Defining a Dock Pane
--------------------

Now we imagine that we are building a very primitive Python IDE and that we
would like to add a dock pane for browsing the local filesystem. We could create
a ``DockPane`` subclass similarly to the ``TaskPane`` above, implementing the
``create_contents(parent)`` method of ``DockPane`` to provide the
toolkit-specific control for the file browser. But if we are familiar with
Traits UI we see that it would be more convenient to use the Traits UI
``FileEditor`` for this purpose. The Tasks framework provides the
``TraitsDockPane`` class to facilitate this. We define the pane as follows::

    from pyface.tasks.api import TraitsDockPane
    from traits.api import Event, File, List, Str
    from traitsui.api import View, Item, FileEditor

    class FileBrowserPane(TraitsDockPane):

        #### TaskPane interface ###############################################

        id = 'example.file_browser_pane'
        name = 'File Browser'

        #### FileBrowserPane interface ########################################

        # Fired when a file is double-clicked.
        activated = Event

        # The list of wildcard filters for filenames.
        filters = List(Str)

        # The currently selected file.
        selected_file = File

        # The view used to construct the dock pane's widget.
        view = View(Item('selected_file',
                         editor=FileEditor(dclick_name='activated',
                                           filter_name='filters'),
                         style='custom',
                         show_label=False),
                    resizable=True)

When a control is needed for the pane, it will be constructed using the standard
Traits UI mechanisms. There exist additional options, not described here, for
specifying a model object, which is often important when building a complex
application. There is also a ``TraitsTaskPane`` class that provides similar
functionality for defining Traits-based central panes. As always, the reader is
referred to the Tasks API documentation for more information.

Now let us amend the example task defined above with a ``create_dock_panes()``
method. This method returns the list of dock pane instances associated with the
task. We also define a method on our task for opening a file in the editor,
which we connect to the dock pane's ``activated`` event::

    class ExampleTask(Task):

        [ ... ]
        
        def create_dock_panes(self):
            """ Create the file browser and connect to its double click event.
            """
            browser = PythonScriptBrowserPane()
            handler = lambda: self.open_file(browser.selected_file)
            browser.on_trait_change(handler, 'activated')
            return [ browser ]

        def open_file(self, filename):
            """ Open the file with the specified path in the central pane.
            """
            self.window.central_pane.editor.path = filename

.. index:: task; layout, PaneItem, TaskLayout, Tabbed, Splitter

Providing a Default Layout
--------------------------

Although dock panes are designed to be moved around and otherwise manipulated by
the user, we often have a particular default layout in mind when designing an
application. The Tasks framework provides the ``TaskLayout`` class to make the
specification of this layout possible. Usually, we are only concerned with four
attributes of this class, namely ``left``, ``right``, ``bottom``, and
``top``. Each of these attributes may be assigned a layout item, which is
either a ``PaneItem``, for specifying a particular dock pane; a ``Tabbed`` item,
containing other ``PaneItem`` instances; or a ``Splitter``, containing arbitrary
subitems.

A few examples should suffice to make this clear. To stack the dock pane with ID
'dock_pane_1' on top of that with ID 'dock_pane_2', with both to the left of the
central pane, one specifies::

    left = Splitter(PaneItem('dock_pane_1'), 
                    PaneItem('dock_pane_2'),
                    orientation='vertical')

.. index:: HSplitter, VSplitter

We could also have used ``VSplitter``, which is a convenient abbreviation for a
splitter with vertical orientation. Similarly, ``HSplitter`` is an abbrevation
for a splitter with horizontal orientation.

To put these dock panes in tab group below the central pane, we might write::

    bottom_panes = Tabbed(PaneItem('dock_pane_1', height=400), 
                          PaneItem('dock_pane_2'))

Observe that we have explicitly provided a height for the first dock
pane. Provided that the dock pane's underlying control does not have a
conflicting minimum or maximum size constraint, Tasks guarantees that it will
honor this height exactly. Of course, if ``width`` or ``height`` are not
provided, Tasks will use the dock pane's toolkit-specific size hint to
determine its size.

Now we will provide our example task with a simple layout using the
``default_layout`` attribute of ``Task``::

    class ExampleTask(Task):

        [ ... ]

        default_layout = TaskLayout(
            left=PaneItem('example.python_script_browser_pane'))

Note that dock panes that do not appear in the layout will not be visible by
default. A task without a default layout is equivalent to a task with an empty
layout; in both cases, only the central pane will be visible by
default. Finally, note that the layout behavior is undefined if a dock pane
appears multiple times in a layout.

.. rubric:: Footnotes

.. [1] For more information about the MVC pattern as used in ETS, the reader is
       referred to the `Introduction
       <http://enthought.github.com/traits/TUIUG/intro.html>`_ of the Traits UI
       User Guide.

.. [2] Throughout this document, "``Task``" will refer to the class of that name
       in the Tasks API, while "task" will be reserved for the general UI
       concept, and similarly for other terms.

.. [3] In this and the subsequent section, we will be referencing (often in
       abbreviated form) the Tasks example code in the TraitsGUI package,
       available `online
       <https://github.com/enthought/traitsgui/tree/master/examples/tasks>`_ and
       in the ETS distribution.
