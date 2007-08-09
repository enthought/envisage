# Major package imports.
from setuptools import setup, find_packages

setup(
    name                 = 'acme.motd.plugin',
    description          = 'The ACME Message of the Day (MOTD) Plugin',
    version              = '0.1a1',
    author               = 'Enthought, Inc',
    author_email         = 'info@enthought.com',
    license              = 'BSD',
    zip_safe             = True,
    packages             = find_packages(),
    include_package_data = True,

    install_requires     = [
        'acme.motd>=0.1a1',
    ],

    entry_points = """

    [enthought.envisage.plugins]
    motd = acme.motd.motd_plugin:MOTDPlugin

    [enthought.envisage.extension_points]
    acme.motd.messages = acme.motd.api:IMessage
    
    """
)
