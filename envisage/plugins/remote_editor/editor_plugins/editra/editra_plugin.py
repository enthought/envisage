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
from traits.api import Any, Bool
from envisage.plugins.remote_editor.editor_plugins.editor_plugin \
        import EditorPlugin

# Editra namespace imports
from wx.tools.Editra.src import ed_menu
from profiler import Profile_Get

# Constants
_ = wx.GetTranslation
ID_RUN_SCRIPT = wx.NewId()
ID_RUN_TEXT = wx.NewId()


class EditraEditorPlugin(EditorPlugin):

    # Client interface

    # Dispatch all command events in same thread as the wx event loop
    ui_dispatch = 'wx'

    # EditraEditorPlugin interface

    # A reference to the Editra mainWindow
    main_window = Any

    # Whether the window should be given focus when it recieves a command
    raise_on_command = Bool(True)

    #--------------------------------------------------------------------------
    # 'EditorPlugin' interface
    #--------------------------------------------------------------------------

    def new(self):
        """ Open a new file in the main window.
        """
        notebook = self.main_window.GetNotebook()
        current = notebook.GetCurrentCtrl()
        if current.GetFileName() != "" or str(current.GetText()) != "":
            notebook.NewPage()
            notebook.GoCurrentPage()
        current.FindLexer('py')
        current.BackSpaceUnIndents = True

        if self.raise_on_command:
            self.main_window.Raise()

    def open(self, filename):
        """ Open the given filename in the main window.
        """
        self.main_window.DoOpen(None, filename)

        if self.raise_on_command:
            self.main_window.Raise()


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

        # Register the EditorPlugin with the Enthought remote_editor server
        self.client = EditraEditorPlugin(main_window=self.mainWindow)
        self.client.register()

        # Set up a handler for keybindings. Ideally, we would do this through an
        # interface provided by Editra, but since this seems to change with
        # every single Editra release, we take the brute force approach.
        mainWindow.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        # Insert menu items
        toolsMenu = menuBar.GetMenuByName("tools")

        mnu_run_text = wx.MenuItem(toolsMenu, ID_RUN_TEXT,
                         _('Execute selection\tShift+Enter'),
                         _('Execute selected text in a python shell'),
                         wx.ITEM_NORMAL)
        mnu_run_text.SetBitmap(wx.Bitmap(os.path.join(
                                    os.path.dirname(__file__),
                                    'images', 'python_runsel_16x16.png')))
        toolsMenu.AppendItem(mnu_run_text, use_bmp=False)

        mnu_run_script = wx.MenuItem(toolsMenu, ID_RUN_SCRIPT,
                         _('Execute script\tCtrl+Enter'),
                         _('Execute file in a python shell'))
        mnu_run_script.SetBitmap(wx.Bitmap(os.path.join(
                                    os.path.dirname(__file__),
                                    'images', 'python_run_16x16.png')))
        toolsMenu.AppendItem(mnu_run_script, use_bmp=False)

        # Bind the events.
        self.mainWindow._handlers['menu'].extend(
            [(ID_RUN_SCRIPT, self.OnRunScript),
                 (ID_RUN_TEXT, self.OnRunText) ])

        # The enable/disable callback for the toolbar button (we need to insert
        # this callback at the front of the stack).
        self.mainWindow._handlers['ui'].insert(0,
            (ID_RUN_TEXT, self.EnableSelection), )

        # Insert toolbar items
        toolBar = mainWindow.GetToolBar()

        self.run_sel_tb = toolBar.AddLabelTool(
            ID_RUN_TEXT, 'Execute selection',
            wx.Bitmap(os.path.join(os.path.dirname(__file__),
                                   'images', 'python_runsel_24x24.png')),
            shortHelp='Execute selection',
            longHelp='Execute selection in shell')

        self.run_file_tb = toolBar.AddLabelTool(
            ID_RUN_SCRIPT, 'Execute',
            wx.Bitmap(os.path.join(os.path.dirname(__file__),
                                   'images', 'python_run_24x24.png')),
            shortHelp='Execute script',
            longHelp='Execute whole file in shell')

        # Just calling AddLabelTool is not displaying the new tools in the
        # toolbar (for Win XP and OS-X at least). Need to call Realize.
        toolBar.Realize()

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



