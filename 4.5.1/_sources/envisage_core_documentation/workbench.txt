Workbench
=========

The workbench plugin, found in the envisage.ui.workbench_ package,
provides a style of user interface that is often (but not exclusively) found in
integrated development environments (IDEs). Note that this does not mean that
all of your user interfaces must fit this pattern -- just that if they do, then
we have done a lot of the work for you.

Workbench user interfaces are based on 3 simple concepts:

1) Views

   Views are primarily used to present information to the user to help them
   perform their current task.

   In an IDE application, views might be:

   - file tree
   - class outlines

2) Editors

   Editors allow the user to manipulate data and objects to perform their
   current task. Editors are really the focus of users attention with the
   views used to provide supporting information. Editors are grouped together
   geographically in what is known as the *editor area*.

   In an IDE application, editors would contain the source code that a 
   developer is currently working on.

3) Perspectives

   A perspective is a particular grouping of views (usually around the editor
   area) that correspond to a user task.

   For example, in an IDE, I might have the following perspectives:

   - Coding perspective

     This is the perspective that the user (in this case a developer) would be
     in when they are actually writing the code. It might contain views that
     show the files in the current project, the outline of the current class
     etc, and the editors would contain the source code that they are actually
     working on.

   - Debugging perspective

     In this perspective, the user would still see the source code in the
     editors, but the views might show things like breakpoints,
     variable watches, stack information etc.

In keeping with the Envisage philosophy of making code as reuseable as
possible, the workbench plugin is just a thin layer over the PyFace Workbench
widget to allow views, editors and perspectives to be contributed via plugins.


.. toctree::
    :maxdepth: 2

    preferences.rst

.. _envisage.ui.workbench: https://github.com/enthought/envisage/tree/master/envisage/ui/workbench/api.py
