# Major package imports.
from setuptools import setup, find_packages

setup(
    name                 = 'acme.bad',
    version              = '0.1a1',
    author               = 'Enthought, Inc',
    author_email         = 'info@enthought.com',
    license              = 'BSD',
    zip_safe             = True,
    packages             = find_packages(),
    include_package_data = True,

    namespace_packages   = [
        'acme',
        'acme.bad'
    ],

    install_requires     = [
        'acme.foo'
    ],

    entry_points = """

    [envisage.plugins]
    acme.bad = acme.bad.bad_plugin:BadPlugin

    """
)
