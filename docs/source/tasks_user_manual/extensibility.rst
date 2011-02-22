.. _extensibility:

.. index:: Envisage

===============
 Extensibility
===============

The foregoing sections have described those elements of the Tasks framework that
belong to the PyFace project; as such, our imports have been from the
``enthought.pyface.tasks`` package. We now discuss how Tasks can be used in
conjunction with Envisage to build extensible applications. Accordingly, our
imports in this section will be from the ``enthought.envisage.ui.tasks``
package.

As remarked in the :ref:`introduction`, some familiarity with the Envisage
plugin framework is assumed. For more information about Envisage, the reader is
referred to the project's `documentation 
<http://enthought.github.com/envisagecore/>`_.

.. _tasks-plugin:

The Tasks Plugin
================

In creating an extensible Tasks application, we imagine two primary
extensibility use cases:

1. **Contributing to an existing task:**

   In this case, the user wishes to add some combination of dock panes, menu
   items, and tool bar buttons to an existing task. In other words, the user
   would like to extend a task's functionality without changing its fundamental
   purpose.

2. **Contributing a new task:**

   Alternatively, the user may find that the none of the existing tasks are
   suitable for the functonality that he or she wishes to implement. Thus the
   user decides to contribute an entirely new task.
   
The Tasks plugin has an extension point corresponding to each of these two use
cases. These extensions points are:

.. index:: TaskFactory

1. ``enthought.envisage.ui.tasks.tasks``:

   A list of ``TaskFactory`` instances. ``TaskFactory`` is a lightweight class
   for associating a task factory with a name and an ID. We shall see an example
   of its use in the following subsection.

.. index:: TaskExtension

2. ``enthought.envisage.ui.tasks.task_extensions``:

   A list of ``TaskExtension`` instances. A ``TaskExtension`` is a bundle of
   menu bar, tool bar, and dock pane additions to an existing task. This class
   is discussed in detail in the subsection on :ref:`extending-a-task`.

The Tasks plugin also provides two extensions points that permit the
creation of extensible preferences dialogs. We defer discussion of this
functionality to the subsection on :ref:`creating-a-preferences-dialog`.

.. _tasks-applications:

.. index:: application, TasksApplication

Creating a Tasks Application
============================

Let us imagine that we are building a (slightly whimsical) application for
visualizing `strange attractors <http://en.wikipedia.org/wiki/Attractor>`_, in
two and three dimensions [1]_. We take for granted the existence of tasks
for performing each of these two kinds of visualization.

Like any Envisage application, our application will contain a ``Plugin``
instance to expose functionality to other plugins. In this case, we will
contribute our two tasks to the Tasks plugin. Because the Tasks plugin is
responsible for creating tasks and the windows that contain them, it expects to
receive *factories* for creating ``Task`` instances rather than the instances
themselves. The ``TaskFactory`` class fulfills this role.

With this in mind, we can define a ``Plugin`` for our application::

    class AttractorsPlugin(Plugin):

        #### 'IPlugin' interface ##############################################

        # The plugin's unique identifier.
        id = 'example.attractors'

        # The plugin's name (suitable for displaying to the user).
        name = 'Attractors'

        #### Contributions to extension points made by this plugin ############

        tasks = List(contributes_to='enthought.envisage.ui.tasks.tasks')

        def _tasks_default(self):
            return [ TaskFactory(id = 'example.attractors.task_2d',
                                 name = '2D Visualization',
                                 factory = Visualize2dTask),
                     TaskFactory(id = 'example.attractors.task_3d',
                                 name = '3D Visualization',
                                 factory = Visualize3dTask) ]

.. index:: application; layout, TaskWindowLayout

Having contributed tasks to the Tasks plugin, we must now specify how the tasks
shall be added to windows to constitute our application. We call this
specification the *application-level layout* to distinguish it from the
lower-level layout attached to a task. Concretely, an application-level layout
consists of a set of ``TaskWindowLayout`` objects, each of which indicates which
tasks are attached to the window, which task is active in the window, and,
optionally, the size and position of the window.

The default application-level layout is defined inside our application class,
which must inherit ``TasksApplication``::

    class AttractorsApplication(TasksApplication):

        #### 'IApplication' interface #########################################

        # The application's globally unique identifier.
        id = 'example.attractors'

        # The application's user-visible name.
        name = 'Attractors'

        #### 'TasksApplication' interface #####################################

        # The default application-level layout for the application.
        default_layout = [ TaskWindowLayout(tasks=['example.attractors.task_2d',
                                                  'example.attractors.task_3d'],
                                            size=(800, 600)) ]

Observe that each of the IDs specified in the layout must correspond to the ID
of a ``TaskFactory`` that has been contributed to the Tasks plugin. Also note
that the ``TaskWindowLayout`` class has an ``active_task`` attribute; by
omitting it, we indicate that the first task in the task list is to be active by
default.

.. index:: application; state restoration

By default, the Tasks framework will restore application-level layout when the
application is restarted. That is, the set of windows and tasks attached to
those windows that is extant when application exits will be restored when
application is started again. If, however, the ``restore_default`` attribute of
the application is enabled, the default application-layout will be restored when
the application is restarted. (Regardless of this setting, the UI layout
*within* individual tasks will be persisted.)

Apart from this functionality, the Tasks plugin provides no additional *default*
behavior for managing tasks and their windows, permitting users to switch tasks
within a window, etc. This is to be expected, as these behaviors are
fundamentally application-specific. That said, we shall see in
:ref:`global-task-extensions` that the Tasks plugins provides a few built-in
extensions for implementing common behaviors.

.. _creating-a-preferences-dialog:

Creating a Preferences Dialog
=============================

TODO

.. _extending-a-task:

Extending an Existing Task
==========================

Contributions are made to an existing task via the ``TaskExtension`` class,
which was briefly introduced above. ``TaskExtension`` is a simple class with
three attributes:

1. ``task_id``: The ID of the task to extend.
2. ``actions``: A list of ``SchemaAddition`` objects.
3. ``dock_panes_factories``: A list of callables for creating dock panes.

.. index:: SchemaAddition

The second attributes requires further discussion. In the previous section, we
remarked that a task's menu and tool bars are defined using schemas; the
``SchemaAddition`` class provides a mechanism for inserting new items into these
schemas.

.. index:: path

A schema implicitly defines a *path* for each of its elements. For example, in
the schema::

    SMenuBar(SMenu(SGroup([ ... ],
                          id = 'SaveGroup'),
                   [ ... ],
                   id = 'File', name = '&File),
             SMenu([ ... ],
                   id = 'Edit', name = '&Edit'))

the edit menu has the path "MenuBar/Edit". Likewise, the save group in the file
menu has the path "MenuBar/File/SaveGroup". We might define an addition for this
menu as follows::

    SchemaAddition(factory = MyContributedGroup,
                   path = 'MenuBar/File')

where ``factory`` is a callable that produces an object from the PyFace action
API, in this case a custom subclass of ``Group`` [2]_.

.. index:: before, after

The group created from the schema addition above would be inserted at the bottom
of the file menu. The ``SchemaAddition`` class provides two further attributes
for specifying with greater precision the location of the insertion: ``before``
and ``after``. Setting one of these attributes to the ID of a schema with the
same path ensures that the insertion will be made before or after, respectively,
that schema. For example, in the expanded addition::

     SchemaAddition(factory = MyContributedGroup,
                    before = 'SaveGroup',
                    path = 'MenuBar/File')

the created group would be inserted before the save group. If both ``before``
and ``after`` are set, Tasks will attempt to honor them [3]_. In the event that
Tasks cannot, the menu order is undefined (although the insertions are
guaranteed to made somewhere) and an error is logged.

.. _global-task-extensions:

Global Task Extensions
=======================

.. index:: global action

When creating an application with several tasks it is frequently the case that
certain menu bar or tool bar actions should be present in all tasks. Such
actions might include an "Exit" item in the "File" menu or an "About" item in
the "Help" menu. One can, of course, include these items in the schemas of each
task; indeed, if the actions require task-specific behavior, this is the only
reasonable approach to take. But for actions that are truly global in nature
Tasks provides an alternative that may be more convenient.

The ``global_actions`` attribute of the ``TasksApplication`` class is a list of
schema additions that will be make to *all* tasks. By default, Tasks provides
the following additions:

- A group of actions in the menu with ID "View" for toggling the visibility of
  dock panes (see ``enthought.pyface.tasks.action.api.DockPaneToggleGroup``)
- A "Preferences" action in the menu with ID "Edit", if the application has any
  preferences panes
- An "Exit" action in the menu with ID "File"

The user is free to override this list, either to supplement it with new schema
additions or to replace it entirely. For example, to provide a simple mechanism
for changing tasks, one might add an addition to the "View" menu with the
builtin task switcher as its factory (see
``enthought.pyface.tasks.action.api.TaskChangeMenuManager``).

.. rubric:: Footnotes

.. [1] In this section, we shall be referencing--often with considerable
       simplification--the Attractors example code in the EnvisagePlugins
       package, available `online
       <https://github.com/enthought/envisageplugins/tree/master/examples/tasks/attractors>`_
       and in the ETS distribution.

.. [2] Note that although schemas are expanded into PyFace action items, they
       belong to a distinct API. It is beyond the scope of this document to
       describe the PyFace action API. For lack of more complete documentation,
       the reader is referred to the `source code
       <https://github.com/enthought/traitsgui/blob/master/enthought/pyface/action/>`_.

.. [3] Tasks differs from the Workbench on this point.
