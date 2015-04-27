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

    namespace_packages   = [
        'acme',
        'acme.motd'
    ],

    install_requires     = [
        'envisage>=3.0.0a1',
    ],

    entry_points = """

    [envisage.plugins]
    acme.motd = acme.motd.motd_plugin:MOTDPlugin

    """
)
