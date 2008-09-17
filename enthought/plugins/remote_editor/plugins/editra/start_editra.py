""" Provides a platform indepedent way to launch Editra. Code mostly copied
    from Editra run file (/usr/bin/editra) in Ubuntu wx package.
"""

import sys
import os
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
    from enthought.plugins.remote_editor.plugins.editra.enshell_editra_plugin \
            import EnShellPlugin
    enshell_plugin = EnShellPlugin(Editra=self)
    try:
        enshell_plugin.do_PlugIt()
        old_MainLoop(self, *args, **kwargs)
    finally:
        enshell_plugin.client.unregister()

Editra.Editra.MainLoop = my_MainLoop

def main():
    Editra.Main()

if __name__ == '__main__':
    main()
