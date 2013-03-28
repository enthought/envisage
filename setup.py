# Copyright (c) 2008-2013 by Enthought, Inc.
# All rights reserved.
from os.path import join
from setuptools import setup, find_packages


info = {}
execfile(join('envisage', '__init__.py'), info)


setup(
    name = 'envisage',
    version = info['__version__'],
    author = "Martin Chilvers, et. al.",
    author_email = "info@enthought.com",
    maintainer = 'ETS Developers',
    maintainer_email = 'enthought-dev@enthought.com',
    url = "http://code.enthought.com/projects/envisage/",
    download_url = ('http://www.enthought.com/repo/ets/envisage-%s.tar.gz' %
                    info['__version__']),
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
        """.splitlines() if len(c.strip()) > 0],
    description = 'extensible application framework',
    long_description = open('README.rst').read(),
    entry_points = """
        [envisage.plugins]
        envisage.core = envisage.core_plugin:CorePlugin
        """,
    ext_modules = [],
    install_requires = info['__requires__'],
    license = "BSD",
    packages = find_packages(),
    package_data = {'': ['images/*', '*.ini',]},
    platforms = ["Windows", "Linux", "Mac OS-X", "Unix", "Solaris"],
    zip_safe = False,
)
