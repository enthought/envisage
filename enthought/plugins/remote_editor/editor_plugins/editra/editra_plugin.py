""" Integrates Editra with the an envisage applciation with the remote editor
plugin.
"""
__author__ = "Enthought"
__version__ = "0.1"

# Standard library imports
import os

# System library imports
import wx

# ETS imports
from enthought.plugins.remote_editor.editor_plugins.editor_plugin \
        import EditorPlugin

# Editra namespace imports
from wx.tools.Editra.src import ed_menu
from profiler import Profile_Get

_ = wx.GetTranslation
ID_RUN_SCRIPT = wx.NewId()
ID_RUN_TEXT = wx.NewId()

class EditraEditorPlugin(EditorPlugin):

    # Client interface
    wx = True

    # EditorPlugin interface

    # a reference to the editra mainWindow
    mainWindow = None

    def new(self):
        """ Open a new file in the main window. """
        notebook = self.mainWindow.GetNotebook()
        current = notebook.GetCurrentCtrl()
        if current.GetFileName() != "" or str(current.GetText()) != "":
            notebook.NewPage()
            notebook.GoCurrentPage()
        current.FindLexer('py')
        current.BackSpaceUnIndents = True

    def open(self, filename):
        """ Open the given filename in the main window. """
        self.mainWindow.DoOpen(None, filename)


class RemoteEditorPlugin(object):
    """ Editor plugin for communicating with shells programs, acting as a
        remote editor.
    """

    def __init__(self, Editra=None):
        self.Editra = Editra


    def do_PlugIt(self):
        self.mainWindow = mainWindow = wx.GetApp().GetMainWindow()
        self.log = wx.GetApp().GetLog()
        self.log("[remote editor][info] Installing remote editor plugin")
        menuBar= mainWindow.GetMenuBar()

        # Register the EditorPlugin with the enthought remote_editor server
        self.client = EditraEditorPlugin(mainWindow=self.mainWindow)
        self.client.register()

        # Set up keybindings
        try:
            # Trying to set up keybindings in a not too ugly way. This
            # sems to be fairly fragile and dependant on the Editra
            # version, so we fall back to a manual way on exception
            keybinder = menuBar.GetKeyBinder()
            script, text = ("Ctrl", "Enter"), ("Shift", "Enter")
            if keybinder.GetCurrentProfile():
                keybinder.SetBinding(ID_RUN_SCRIPT, script)
                keybinder.SetBinding(ID_RUN_TEXT, text)
            else:
                # Ugh. SetBinding does nothing if no profile is loaded, as of
                # Editra version 0.3.38.
                ed_menu._DEFAULT_BINDING[ID_RUN_SCRIPT] = script
                ed_menu._DEFAULT_BINDING[ID_RUN_TEXT] = text
                keybinder.LoadDefaults()
            runScriptMenuText = keybinder.GetBinding(ID_RUN_SCRIPT)
            runTextMenuText = keybinder.GetBinding(ID_RUN_TEXT)
        except:
            mainWindow.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
            runTextMenuText = _("\tShift+Enter")
            runScriptMenuText = _("\tCtrl+Enter")

        # Insert menu items
        toolsMenu = menuBar.GetMenuByName("tools")

        mnu_run_text = wx.MenuItem(toolsMenu, ID_RUN_TEXT,
                         _('Execute selection') + runTextMenuText,
                         _('Execute selected text in a python shell'),
                         wx.ITEM_NORMAL)
        mnu_run_text.SetBitmap(wx.Bitmap(os.path.join(
                                    os.path.dirname(__file__), 
                                    'images', 'python_runsel_16x16.png')))
        toolsMenu.AppendItem(mnu_run_text, use_bmp=False)

        mnu_run_script = wx.MenuItem(toolsMenu, ID_RUN_SCRIPT,
                         _('Execute script') + runScriptMenuText,
                         _('Execute file in a python shell'))
        mnu_run_script.SetBitmap(wx.Bitmap(os.path.join(
                                    os.path.dirname(__file__), 
                                    'images', 'python_run_16x16.png')))
        toolsMenu.AppendItem(mnu_run_script, use_bmp=False)
        
        # Bind the events.
        self.mainWindow._handlers['menu'].extend(
            [(ID_RUN_SCRIPT, self.OnRunScript),
                 (ID_RUN_TEXT, self.OnRunText) ])
        

        # The enable/disable callback for the toolbar button (we
        # need to insert this callback at the front of the stack).
        self.mainWindow._handlers['ui'].insert(0,
            (ID_RUN_TEXT, self.EnableSelection), )

        # Insert toolbar items
        toolBar = mainWindow.GetToolBar()
        self.run_sel_tb = toolBar.AddLabelTool(ID_RUN_TEXT, 
                            'Execute selection', 
                            wx.Bitmap(os.path.join(
                                    os.path.dirname(__file__), 
                                    'images', 'python_runsel_24x24.png')),
                            shortHelp='Execute selection',
                            longHelp='Execute selection in shell',
                            )
        self.run_file_tb = toolBar.AddLabelTool(ID_RUN_SCRIPT, 'Execute', 
                            wx.Bitmap(os.path.join(
                                    os.path.dirname(__file__), 
                                    'images', 'python_run_24x24.png')),
                            shortHelp='Execute script',
                            longHelp='Execute whole file in shell',
                            )
        # For some reason, just calling AddLabelTool is not displaying the new
        # tools in the toolbar (for Win XP at least). 
        # Calling ReInit re-initializes all the tools and
        # the new tools show up. This is probably related to the bitmaps we are
        # passing in for the new tools. 
        # Source code forEdToolBar is in: 
        # http://www.editra.org/docs/editra_api/Editra.src.ed_toolbar-pysrc.html
        toolBar.ReInit()

    def OnRunScript(self, event):
        """ Run the script, prompting for a save if necessary.
        """
        notebook = self.mainWindow.GetNotebook()
        currentTab = notebook.GetCurrentCtrl()
        filename = currentTab.GetFileName()
        if filename == "":
            if self.mainWindow.OnSaveAs(None, page=currentTab):
                filename = currentTab.GetFileName()
            else:
                return
        else:
            if currentTab.GetModify():
                result = notebook.frame.ModifySave()
                if result == wx.ID_CANCEL:
                    return
        self.client.send_command('run_file', filename)

    def OnRunText(self, event):
        """ Run the selected text.
        """
        currentTab = self.mainWindow.GetNotebook().GetCurrentCtrl()
        text = str(currentTab.GetSelectedText()) # Convert from unicode
        if text == "":
            msg = _("Cannot execute. No text is selected.")
            self.mainWindow.PushStatusText(msg)
        else:
            self.client.send_command('run_text', text)

    def OnKeyDown(self, event):
        """ Handles key presses when the version of Editra is less than
            0.3 (no KeyBindings support).
        """
        if event.GetKeyCode() == wx.WXK_RETURN:
            if event.ShiftDown():
                self.OnRunText(event)
            elif event.ControlDown():
                self.OnRunScript(event)
        else:
            event.Skip()

    def EnableSelection(self, evt):
        if not self.mainWindow.IsActive():
            return

        e_id = evt.GetId()
        evt.SetMode(wx.UPDATE_UI_PROCESS_SPECIFIED)
        # Slow the update interval to reduce overhead
        evt.SetUpdateInterval(200)
        ctrl = self.mainWindow.nb.GetCurrentCtrl()
        if e_id == ID_RUN_TEXT:
            evt.Enable(ctrl.GetSelectionStart() != ctrl.GetSelectionEnd())
        else:
            evt.Skip()

 
   
