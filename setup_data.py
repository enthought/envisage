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
APPTOOLS = etsdep('AppTools', '3.1.1')
CHACO = etsdep('Chaco', '3.0.2')
ENVISAGECORE = etsdep('EnvisageCore', '3.0.2')
ETSDEVTOOLS_FBI = etsdep('ETSDevTools[fbi]', '3.0.2')  # -- only by the debug/fbi_plugin.py
TRAITSGUI = etsdep('TraitsGUI', '3.0.4')
TRAITS_UI = etsdep('Traits[ui]', '3.0.4')


# A dictionary of the setup data information.
INFO = {
    'extras_require' : {
        'chaco': [
            CHACO,
            ],
        'debug': [
            ETSDEVTOOLS_FBI,
            ],

        # All non-ets dependencies should be in this extra to ensure users can
        # decide whether to require them or not.
        'nonets': [
            #'wx ==2.6',  # wx not available in egg format on all platforms.
            ],
        },
    'install_requires' : [
        APPTOOLS,
        ENVISAGECORE,
        TRAITSGUI,
        TRAITS_UI,
        ],
    'name': 'EnvisagePlugins',
    'version': '3.0.2',
    }
