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

    namespace_packages   = [
        'acme',
        'acme.bar'
    ],

    install_requires     = [
        'acme.foo'
    ],

    entry_points = """

    [enthought.envisage.plugins]
    bar = acme.bar.bar_plugin:BarPlugin
    
    """
)
