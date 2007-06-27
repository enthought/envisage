# Major package imports.
from setuptools import setup, find_packages

setup(
    name                 = 'acme.motd',
    version              = '0.1a1',
    author               = 'Enthought, Inc',
    author_email         = 'info@enthought.com',
    license              = 'BSD',
    zip_safe             = True,
    packages             = find_packages(),
    include_package_data = True,

    namespace_packages   = ['acme'],
    install_requires     = ['enthought.envisage.core'],

    entry_points = """

    [enthought.envisage.plugins]
    motd = acme.motd.motd_plugin:MOTDPlugin
    
    """
)
