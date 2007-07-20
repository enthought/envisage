from setuptools import setup, find_packages


setup(
    name                 = "enthought.envisage",
    version              = "3.0a1",
    description          = "Envisage - An Extensible Application Framework",
    url                  = "http://code.enthought.com/enstaller",
    license              = "BSD",
    zip_safe             = False,
    packages             = find_packages(),
    ext_modules          = [],
    include_package_data = True,

    namespace_packages   = [
        "enthought",
        "enthought.envisage"
    ],

    install_requires     = [
        "enthought.traits>=3.0.0b1",
        "enthought.util"
    ]
)
