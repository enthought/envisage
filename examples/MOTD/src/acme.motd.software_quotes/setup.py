# Major package imports.
from setuptools import setup, find_packages

setup(
    name                 = 'acme.motd.software_quotes',
    version              = '0.1a1',
    author               = 'Enthought, Inc',
    author_email         = 'info@enthought.com',
    license              = 'BSD',
    zip_safe             = True,
    packages             = find_packages(),
    include_package_data = True,

    namespace_packages   = [
        'acme',
        'acme.motd',
        'acme.motd.software_quotes'
    ],

    install_requires     = [
        'acme.motd',
    ],

    entry_points = """

    [enthought.envisage.preferences]
    pkgfile://acme.motd.software_quotes/preferences.ini = preferences

    """

    
)
