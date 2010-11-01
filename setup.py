#!/usr/bin/env python
#
# Copyright (c) 2008-2009 by Enthought, Inc.
# All rights reserved.


"""
Plug-ins for the Envisage framework.

The EnvisagePlugins project includes a number of plug-ins for the Envisage
framework that Enthought has found useful for building scientific applications.
Envisage does not require that you use these plug-ins, but you may find them
useful to avoid having to reinvent these particular wheels.

- **Workbench**: Provides an application GUI window that supports views and
  perspectives, similar to the Eclipse IDE.
- **Action**: Supports user-interaction command mechanisms, such as toolbars,
  menus, and buttons.
- **Single Project**: Supports a project paradigm for saving application data,
  assuming an interaction model in which only one project can be open in the
  application at a time.
- **Text Editor**: Provides a rudimentary text editor interface.
- **Python Shell**: Provides an interactive Python shell within a
  Workbench-based application.
- **Debug**: Provides the Frame Based Inspector from the ETSDevTools project 
  as an Envisage plug-in.

Prerequisites
-------------
If you want to build EnvisagePlugins from source, you must first install 
`setuptools <http://pypi.python.org/pypi/setuptools/0.6c8>`_.

"""

import traceback
import sys

from distutils import log
from distutils.command.build import build as distbuild
from setuptools import setup, find_packages
from setuptools.command.develop import develop


# FIXME: This works around a setuptools bug which gets setup_data.py metadata
# from incorrect packages. Ticket #1592
#from setup_data import INFO
setup_data = dict(__name__='', __file__='setup_data.py')
execfile('setup_data.py', setup_data)
INFO = setup_data['INFO']


# Pull the description values for the setup keywords from our file docstring.
DOCLINES = __doc__.split("\n")

# The actual setup call
setup(
    author = 'Martin Chilvers, et. al.',
    author_email = 'martin@enthought.com',
    download_url = (
        'http://www.enthought.com/repo/ETS/EnvisagePlugins-%s.tar.gz' %
        INFO['version']),
    classifiers = [c.strip() for c in """\
        Development Status :: 5 - Production/Stable
        Intended Audience :: Developers
        Intended Audience :: Science/Research
        License :: OSI Approved :: BSD License
        Operating System :: MacOS
        Operating System :: Microsoft :: Windows
        Operating System :: OS Independent
        Operating System :: POSIX
        Operating System :: Unix
        Programming Language :: Python
        Topic :: Scientific/Engineering
        Topic :: Software Development
        Topic :: Software Development :: Libraries
        """.splitlines() if len(c.split()) > 0],
    description = DOCLINES[1],
    entry_points = '''
        [enthought.envisage.plugins]
        enthought.envisage.ui.workbench = enthought.envisage.ui.workbench.workbench_plugin:WorkbenchPlugin
        enthought.plugins.python_shell = enthought.plugins.python_shell.python_shell_plugin:PythonShellPlugin
        enthought.envisage.developer = enthought.envisage.developer.developer_plugin:DeveloperPlugin
        enthought.envisage.developer.ui = enthought.envisage.developer.ui.developer_ui_plugin:DeveloperUIPlugin
        ''',
    extras_require = INFO['extras_require'],
    ext_modules = [],
    include_package_data = True,
    package_data = {'enthought': [
            'envisage/ui/workbench/*.ini',
            'envisage/ui/workbench/action/images/*.png']},
    install_requires = INFO['install_requires'],
    license = 'BSD',
    long_description = '\n'.join(DOCLINES[3:]),
    maintainer = 'ETS Developers',
    maintainer_email = 'enthought-dev@enthought.com',
    name = 'EnvisagePlugins',
    namespace_packages = [
        'enthought',
        'enthought.envisage',
        'enthought.plugins',
        ],
    packages = find_packages(exclude=['examples']),
    platforms = ["Windows", "Linux", "Mac OS-X", "Unix", "Solaris"],
    tests_require = [
        'nose >= 0.10.3',
        ],
    test_suite = 'nose.collector',
    url = 'http://code.enthought.com/projects/envisage_plugins.php',
    version = INFO['version'],
    zip_safe = False,
    )

