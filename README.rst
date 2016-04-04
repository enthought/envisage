==========================================
envisage: extensible application framework
==========================================

.. image:: https://travis-ci.org/enthought/envisage.png
   :alt: Build Status
   :target: https://travis-ci.org/enthought/envisage

.. image:: http://codecov.io/github/enthought/envisage/coverage.svg?branch=master 
   :target: http://codecov.io/github/enthought/envisage?branch=master

http://docs.enthought.com/envisage

Envisage is a Python-based framework for building extensible applications,
that is, applications whose functionality can be extended by adding "plug-ins".
Envisage provides a standard mechanism for features to be added to an
application, whether by the original developer or by someone else. In fact,
when you build an application using Envisage, the entire application consists
primarily of plug-ins. In this respect, it is similar to the Eclipse and
Netbeans frameworks for Java applications.

Each plug-in is able to:

- Advertise where and how it can be extended (its "extension points").
- Contribute extensions to the extension points offered by other plug-ins.
- Create and share the objects that perform the real work of the application
  ("services").

The Envisage project provides the basic machinery of the Envisage
framework. This project contains no plug-ins. You are free to use:

- plug-ins from the EnvisagePlugins project
- plug-ins from other ETS projects that expose their functionality as plug-ins
- plug-ins that you create yourself

Prerequisites
-------------

* `traits <https://github.com/enthought/traits>`_
