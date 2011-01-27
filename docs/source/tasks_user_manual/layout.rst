=======================
 Window Layout
=======================
First and foremost, the Tasks plugin is designed to facilitate the layout of
modern, customizable user interfaces. Accordingly, we shall begin by learning
how to use Tasks to perform basic window layout.

Lifecycle of a Task
-------------------
The Tasks plugin adheres to the model-view-controller (MVC) design pattern [1]_;
the ``Task`` class functions as the controller and the ``TaskWindow`` class as
the view, with the model being application-specific [2]_. Insofar as a ``Task``
is a controller, it does not itself instantiate or contain any GUI controls,
although it does provide factories and a default layout for the controls it that
manages. Controls are instantiated when a ``Task`` is assigned to a
``TaskWindow``. Specifically, the following actions are taken at this time:

1. The task's central pane is constructed and attached to the window
2. All of the task's dock panes are constructed, even if they are not by default
   visible
3. The visible dock panes laid out around the central pane according to the
   task's default layout or persisted UI state information

While the ``Task`` remains connected to the ``TaskWindow``, neither its central
pane nor its dock panes will be destroyed. If the user "closes" a dock pane, the
pane will be merely hidden, and can be re-activated via the application's View
menu. Only when the ``Task`` itself is closed---that is, when it is removed from
the ``TaskWindow``---will its panes be destroyed. This marks the end of the
``Task``'s lifecycle. If the ``Task`` is to be re-used, a new instance must be
constructed.

Defining a Task
---------------

Defining a Dock Pane
--------------------

.. rubric:: Footnotes
.. [1] For more information about the MVC pattern as used in ETS, the reader is 
       referred to the Introduction of the Traits UI User Guide.
.. [2] Throughout this document, "``Task``" will refer to the class of that name
       in the Tasks API, while "task" will be reserved for the general UI
       concept, and similarly for other terms.
