.. _introduction:

==============
 Introduction
==============

Tasks is an extensible, toolkit-independent framework for building scriptable,
task-oriented user interfaces. This document describes its concepts and design
principles, surveys the classes in its API, and provides a brief tutorial
illustrating its use.

We assume that the reader has a basic familiarity with the concepts of Traits
and Traits UI. These packages are well documented in their respective user
manuals. In the Extensibility section of this document, some additional
knowledge of the Envisage plugin framework is assumed.

For more detailed information concerning the Tasks API, the reader is referred
to the Tasks API Reference.

What is a Task?
---------------

.. index:: task, pane
.. _what-is-a-task:

For the purposes of this document, a *task* is a collection of user interface
elements, called *panes*, which are present in a single window, unified by a
specific purpose, and possessed of a certain structure. In addition, a task may
provide menus, toolbars, and configuration options appropriate for these 
elements.

.. index:: central pane

At the heart of every task is its *central pane*, which exposes its core
functionality. The central pane is always visible and occupies the center of the
window. For example, in an IDE there will be at least one task concerned with
writing code. A code editing widget would constitute the central pane for this
task. If the IDE also provided a GUI construction task (i.e., a WYSIWYG user
interface builder ala Glade or Qt Designer), the central pane would consist of
the "canvas" upon which the user arranges UI elements.

.. index:: dock pane

In addition to the central pane, a task may include any number of subsidiary
panes. These panes are arranged around the central pane in various *dock areas*,
for which reason they are called *dock panes*. Dock panes provide
functionality that is relevant but unessential to the task at hand. For
example, in the code editing task described above, the list of dock panes might
include a file browser, a context-sensitive documentation window, a compilation
log, and a debugger. In general, dock panes can be moved from one dock area to
another, can be made visible or hidden, and can be detached from the main
window.

Historical Background
---------------------

.. index:: background, Workbench
.. _historical-background:

Many of the ideas behind Tasks plugin originate in another Envisage plugin,
called the Workbench (which, in turn, took considerable inspiration from
Eclipse). Indeed, the Tasks plugin has been created largely to serve as a
replacement for the Workbench, borrowing its more useful features while
replacing those which experience has indicated to be cumbersome or
inflexible. The most significant of these issues include:

- **A lack of distinction between the semantics of UI elements and the layout of
  those elements.** A perspective (the Workbench analogue of a task) has very
  little responsibility besides saving the state the user interface. Views
  (the analogues of dock panes) are added directly to the Workbench, which means
  that they cannot be restricted to certain perspectives, nor can a perspective
  exercise meaningful control over the layout of its views. Furthermore,
  recourse must often be made to application-level globals when communicating
  between views, as there is no structure imposed on them by the active
  perspective. Finally, since the application menus are not connected to
  perspectives, there can be only a single set of menu items during the entire
  application lifecycle.

- **A non-customizable central pane.** The notion of editors is inextricably
  connected to the Workbench; the central pane must be a notebook-style
  collection of editors.

The above are design considerations that could not be remedied without a vast
degree of backwards-incompatible change. Less systemic deficiencies of the
Workbench include:

- A lack of robust support for multi-window applications
- An inflexible API for exposing user-configurable preferences

Tasks has been designed specifically to avoid these issues.
