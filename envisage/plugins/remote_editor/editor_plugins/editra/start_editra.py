""" Provides a platform indepedent way to launch Editra. Code mostly copied
    from Editra run file (/usr/bin/editra) in Ubuntu wx package.
"""

import sys
import os

try:
    import Editra as Editra_root
    sys.path.insert(0, os.path.join(os.path.dirname(Editra_root.__file__),
                    'src'))
    # Really ugly: we need to remove the Editra name from the list of
    # imported modules
    sys.modules.pop('Editra')
except ImportError:
    import wx.tools

    # Editra needs its src package to be on the sys.path for plugins and
    # such to work right, so put it there before we do the first import of
    # any Editra package or module.
    sys.path.insert(0, os.path.join(os.path.dirname(wx.tools.__file__),
                                    'Editra', 'src'))

import Editra

# XXX: Super ugly: monkey-patch the main Editra class to add our plugins
old_MainLoop = Editra.Editra.MainLoop

def my_MainLoop(self, *args, **kwargs):
    from envisage.plugins.remote_editor.editor_plugins.editra.editra_plugin \
            import RemoteEditorPlugin
    plugin = RemoteEditorPlugin(Editra=self)
    try:
        plugin.do_PlugIt()
        old_MainLoop(self, *args, **kwargs)
    finally:
        plugin.client.unregister()

Editra.Editra.MainLoop = my_MainLoop

def main():
    Editra.Main()

if __name__ == '__main__':
    main()
