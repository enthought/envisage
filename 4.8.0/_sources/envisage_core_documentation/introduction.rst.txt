Introduction
============

Welcome to the Envisage Project! The goal of the project is to provide a
framework for building extensible, pluggable applications, and in particular
(but not limited to!), extensible, pluggable applications for scientists and
engineers.

The project is really divided into 3 sub-projects:-

1) Core_

   The Envisage Core, found in the top-level envisage_ package,
   defines the basic application architecture including the plugin and
   extension mechanisms. All of the other sub-projects are simply collections
   of plugins that are built on top of the core.

2) User Interface (UI)

   This is small (but hopefully expanding) set of plugins useful for building
   applications with (graphical) User Interfaces. It is found in the
   *envisage.ui* package (and its subpackages), and aims to provide
   functionality commonly required in this type of application including
   actions, menubars, toolbars, user preferences, wizards etc. One of the most
   useful plugins in this project is the Workbench_ plugin (found in the
   envisage.ui.workbench_ package) that helps you build a style of
   user interface that is often (but not exclusively) found in integrated
   development environments (IDEs).

3) Science/Enginneering

   This is the holy grail, and in truth, we haven't got much here yet, but the
   goal is to build up a set of plugins targeted towards scientific and
   engineering applications (data import/export, 2D/3D visualization etc).

Before you read any further, we should point out that Envisage is based
*heavily* on the excellent work that has been done in the Java community on
frameworks such as OSGi_, Eclipse_ (which is built on top of its own OSGi_
implementation) and NetBeans_. Like these other frameworks, Envisage helps you
build applications that are based on the concept of plugins. However, one of
the main goals is to provide a simplified system so that applications and
plugins can be written by scientists, engineers, and those people whose
full-time job is *not* necessarily software development, hence a lot of work
has gone into trying to satify the old adage of "make simple things simple, and
complex things possible". It will obviously be up to you to judge if we
succeeded!

Getting Started
---------------

The best way to get started is probably to take the time to read and digest the
Core_ documentation and then work through the `Hello World`_ and
`Message of the Day`_ examples. Despite being extremely simple, the examples
introduces you to *all* of the fundamental concepts of Envisage, and the *real*
applications that you build (which will hopefully be a lot more useful) will be
built in exactly the same way.

For definitions of the terminology used in Envisage, see the Glossary_
(although it will probably make more sense after going through the other
documentation and examples first).

.. _API: api/index.html
.. _Core: core.html
.. _Eclipse: http://www.eclipse.org
.. _Glossary: Glossary.html
.. _`Message of the Day`: message_of_the_day.html
.. _NetBeans: http://www.netbeans.org
.. _OSGi: http://www.osgi.org
.. _Workbench: Workbench.html

.. _`Hello World`: https://github.com/enthought/envisage/tree/master/examples/Hello_World/hello_world.py

.. _envisage: https://github.com/enthought/envisage/tree/master/envisage/api.py

.. _envisage.ui.workbench: https://github.com/enthought/envisage/tree/master/envisage/ui/workbench/api.py
