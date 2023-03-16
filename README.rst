==========================================
envisage: extensible application framework
==========================================

Documentation: https://docs.enthought.com/envisage

Envisage is a Python-based framework for building extensible applications,
that is, applications whose functionality can be extended by adding "plug-ins".
Envisage provides a standard mechanism for features to be added to an
application, whether by the original developer or by someone else. In fact,
when you build an application using Envisage, the entire application consists
primarily of plug-ins. In this respect, it is similar to the Eclipse and
Netbeans frameworks for Java applications.

Each plug-in is able to:

- Advertise where and how it can be extended (its "extension points").
- Contribute extensions to the extension points offered by other plug-ins or
  its own.
- Create and share the objects that perform the real work of the application
  ("services").

The Envisage project provides the basic machinery of the Envisage
framework. You are free to use:

- the envisage ``CorePlugin`` available through the
  `envisage.api <https://github.com/enthought/envisage/blob/main/envisage/api.py>`__ module
- plug-ins from the envisage
  `plugins <https://github.com/enthought/envisage/tree/main/envisage/plugins>`__ module
- plug-ins from other ETS projects that expose their functionality as plug-ins
- plug-ins that you create yourself

Prerequisites
-------------

The supported versions of Python are Python >= 3.7.  Envisage requires:

* `apptools <https://pypi.org/project/apptools/>`_
* `traits <https://pypi.org/project/traits/>`_

Envisage has the following optional dependencies:

* `Pyface <https://pypi.org/project/pyface/>`_
* `TraitsUI <https://pypi.org/project/traitsui/>`_

To build the full documentation one needs:

* `Sphinx <https://pypi.org/project/Sphinx>`_ version 2.1 or later.
* The `Enthought Sphinx Theme <https://pypi.org/project/enthought-sphinx-theme>`_.
