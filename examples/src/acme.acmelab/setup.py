# Major package imports.
from setuptools import setup, find_packages

setup(
    name                 = 'acme.acmelab',
    version              = '0.1a1',
    author               = 'Enthought, Inc',
    author_email         = 'info@enthought.com',
    license              = 'BSD',
    zip_safe             = True,
    packages             = find_packages(),
    include_package_data = True,

    namespace_packages   = [
        'acme',
        'acme.acmelab'
    ],

    install_requires     = [
        'enthought.envisage.ui.workbench>=3.0a1'
    ],
)
