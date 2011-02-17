.. _extensibility:

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
plugin framework is assumed in this section.

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

1. 'enthought.envisage.ui.tasks.tasks':

   A list of ``TaskFactory`` instances. ``TaskFactory`` is a lightweight class
   for associating a task factory with a name and an ID. We shall see an example
   of its use in the following subsection.

.. index:: TaskExtension

2. 'enthought.envisage.ui.tasks.task_extensions':

   A list of ``TaskExtension`` instances. A ``TaskExtension`` is a bundle of
   menu bar, tool bar, and dock pane additions to an existing task. This class
   is discussed in detail in the subsection on :ref:`extending-a-task`.

.. _tasks-applications:

Creating a Tasks Application
============================

.. _extending-a-task:

Extending an Existing Task
==========================

