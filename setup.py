from setuptools import setup, find_packages


setup(
    name                 = "enthought.envisage3",
    version              = "3.0a1",
    description          = "Envisage - An Extensible Application Framework",
    url                  = "http://code.enthought.com/enstaller",
    license              = "BSD",
    zip_safe             = False,
    packages             = find_packages(),
    ext_modules          = [],
    include_package_data = True,

    install_requires     = [
    ],
    
    namespace_packages = [
        "enthought",
        "enthought.envisage3",
    ],
)
