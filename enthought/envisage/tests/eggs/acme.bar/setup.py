# Major package imports.
from setuptools import setup, find_packages

setup(
    name                 = 'acme.bar',
    version              = '0.1a1',
    author               = 'Enthought, Inc',
    author_email         = 'info@enthought.com',
    license              = 'BSD',
    zip_safe             = True,
    packages             = find_packages(),
    include_package_data = True,

    install_requires     = ['acme.foo'],
    namespace_packages   = ['acme'],

    entry_points = """

    [enthought.envisage.plugins]
    bar = acme.bar.bar_plugin:BarPlugin
    
    """
)
