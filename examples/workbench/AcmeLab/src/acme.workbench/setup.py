# Major package imports.
from setuptools import setup, find_packages

setup(
    name                 = 'acme.workbench',
    version              = '0.1a1',
    author               = 'Enthought, Inc',
    author_email         = 'info@enthought.com',
    license              = 'BSD',
    zip_safe             = True,
    packages             = find_packages(),
    include_package_data = True,

    namespace_packages   = [
        'acme',
        'acme.workbench'
    ],

    install_requires     = [
        'enthought.envisage.ui.workbench>=3.0a1'
    ],

    entry_points         = """

    [enthought.envisage.plugins]
    workbench = acme.workbench.api:WorkbenchPlugin

    """
    
)
