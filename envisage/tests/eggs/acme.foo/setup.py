# Major package imports.
from setuptools import setup, find_packages

setup(
    name                 = 'acme.foo',
    version              = '0.1a1',
    author               = 'Enthought, Inc',
    author_email         = 'info@enthought.com',
    license              = 'BSD',
    zip_safe             = True,
    packages             = find_packages(),
    include_package_data = True,

    namespace_packages   = [
        'acme',
        'acme.foo'
    ],

    install_requires     = [
    ],

    entry_points = """

    [envisage.plugins]
    acme.acme = acme.foo.acme_plugin:AcmePlugin
    acme.foo = acme.foo.foo_plugin:FooPlugin

    """
)
