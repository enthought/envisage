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

    install_requires     = ['acme.bar'],
    namespace_packages   = ['acme'],

    entry_points = """

    [enthought.envisage.plugins]
    baz = acme.baz.baz_plugin:BazPlugin
    
    """
)
