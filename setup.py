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
DEVTOOLS = etsdep('DevTools', '3.0.0b1')
ENABLE_WX = etsdep('Enable[wx]', '3.0.0b1')
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
        ''',
    extras_require = {
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
        CHACO,
        DEVTOOLS,
        ENABLE_WX,
        ENVISAGECORE,
        TRAITS_UI,
        TRAITSGUI,
        ],
    license = 'BSD',
    name = 'EnvisagePlugins',
    namespace_packages = [
        'enthought',
        'enthought.envisage',
        'enthought.envisage.ui',
        'enthought.plugins',
        ],
    packages = find_packages(exclude=['examples']),
    url = 'http://code.enthought.com/envisage',
    version = '3.0.0a1',
    zip_safe = False,
    )
