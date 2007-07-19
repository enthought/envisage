from setuptools import setup, find_packages


setup(
    name                 = "enthought.envisage.ui.action",
    version              = "3.0a1",
    description          = "The Envisage Action Framework",
    url                  = "http://code.enthought.com/enstaller",
    license              = "BSD",
    zip_safe             = False,
    packages             = find_packages(),
    ext_modules          = [],
    include_package_data = True,

    namespace_packages   = [
        "enthought",
        "enthought.envisage",
        "enthought.envisage.ui",
        "enthought.envisage.ui.action",
    ],

    install_requires     = [
        "enthought.envisage.ui.workbench>=3.0a1",
    ],

    entry_points = """

    [enthought.envisage.plugins]
    action = enthought.envisage.ui.action.action_plugin:ActionPlugin
    
    """
)
