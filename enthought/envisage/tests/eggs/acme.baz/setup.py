# Major package imports.
from setuptools import setup, find_packages

setup(
    name                 = 'acme.baz',
    version              = '0.1a1',
    author               = 'Enthought, Inc',
    author_email         = 'info@enthought.com',
    license              = 'BSD',
    zip_safe             = True,
    packages             = find_packages(),
    include_package_data = True,

    namespace_packages   = [
        'acme',
        'acme.baz'
    ],

    install_requires     = [
        'acme.bar'
    ],

    entry_points = """

    [enthought.envisage.plugins]
    acme.baz = acme.baz.baz_plugin:BazPlugin

    """
)
