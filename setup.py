from setuptools import setup, find_packages


# Function to convert simple ETS project names and versions to a requirements
# spec that works for both development builds and stable builds.  Allows
# a caller to specify a max version, which is intended to work along with
# Enthought's standard versioning scheme -- see the following write up:
#    https://svn.enthought.com/enthought/wiki/EnthoughtVersionNumbers
def etsdep(p, min, max=None, literal=False):
    require = '%s >=%s.dev' % (p, min)
    if max is not None:
        if literal is False:
            require = '%s, <%s.a' % (require, max)
        else:
            require = '%s, <%s' % (require, max)
    return require


# Declare our ETS project dependencies.
APPTOOLS = etsdep('AppTools', '3.0.0b1')
CHACO = etsdep('Chaco', '3.0.0b1')
DEVTOOLS_FBI = etsdep('DevTools[fbi]', '3.0.0b1')  # -- only by the debug/fbi_plugin.py
ENVISAGECORE = etsdep('EnvisageCore', '3.0.0b1')
TRAITSGUI = etsdep('TraitsGUI', '3.0.0b1')
TRAITS_UI = etsdep('Traits[ui]', '3.0.0b1')


setup(
    author = 'Martin Chilvers',
    author_email = 'info@enthought.com',
    dependency_links = [
        'http://code.enthought.com/enstaller/eggs/source',
        ],
    description = 'The Envisage Action Framework',
    entry_points = '''
        [enthought.envisage.plugins]
        workbench = enthought.envisage.ui.workbench.workbench_plugin:WorkbenchPlugin
        shell = enthought.plugins.python_shell.python_shell_plugin:PythonShellPlugin
        developer = enthought.envisage.developer.developer_plugin:DeveloperPlugin
        developer_ui = enthought.envisage.developer.ui.developer_ui_plugin:DeveloperUIPlugin
        ''',
    extras_require = {
        'chaco': [
            CHACO,
            ],
        'debug': [
            DEVTOOLS_FBI,
            ],

        # All non-ets dependencies should be in this extra to ensure users can
        # decide whether to require them or not.
        'nonets': [
            #'wx ==2.6',  # wx not available in egg format on all platforms.
            ],
        },
    ext_modules = [],
    include_package_data = True,
    install_requires = [
        APPTOOLS,
        ENVISAGECORE,
        TRAITSGUI,
        TRAITS_UI,
        ],
    license = 'BSD',
    name = 'EnvisagePlugins',
    namespace_packages = [
        'enthought',
        'enthought.envisage',
        'enthought.plugins',
        ],
    packages = find_packages(exclude=['examples']),
    url = 'http://code.enthought.com/envisage',
    version = '3.0.0b1',
    zip_safe = False,
    )
