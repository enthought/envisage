""" Implementation of the plt commands for Envisage. """

import exceptions
import warnings
warnings.filterwarnings('ignore', category=exceptions.FutureWarning)

from enthought.chaco.plot_component import PlotComponent
from enthought.chaco.plt import *
from enthought.enable.wx import Window
from enthought.envisage.ui import Editor, UIPlugin
from enthought.traits.api import Any, Instance, true

class EditorProxyFrame(Editor):
    """ An envisage editor which holds the plot. """
    
    # The EditorShellPlotFrame that owns this EditorProxyFrame.
    parentPlotFrame = Any
    
    def __init__(self, **traits):
        """ Constructor.

        This is not necessary except to facilitate monitoring of object
        construction/destruction with Enthought-internal tools.
        """
        super(EditorProxyFrame, self).__init__(**traits)

        return

    def _create_contents(self, parent):
        """ Create the window contents. """

        self._contents = Window(parent,
                                component=self.parentPlotFrame._component)
        
        return self._contents

    def _closing_changed(self):
        """ Handle the editor closing. """

        # Do a few things to try to help the garbage collector out.
        self._contents.control.Destroy()
        self._contents.control = None
        self._contents = None

        return

class EditorShellPlotFrame(ShellPlotFrame):
    """ A ShellPlotFrame which delegates to an Envisage editor. """

    # The delegated editor.
    delegate = Instance(EditorProxyFrame)

    # Status of the proxy object.
    proxy_object_alive = true
    
    def __init__(self, title):
        """ Constructor. """
        
        # Initialize the editor part of the window.
        self.delegate = editor_factory(
            parentPlotFrame=self,
            title=title,
            parent=UIPlugin.instance.active_window.control
        )
        
        # Initialize the shell plot frame.
        ShellPlotFrame.__init__(self, title)
        
        # Listen for the window closing, so we can clean up.
        self.delegate.on_trait_change(self.on_close, 'closing')

        # Display the delegate.
        self.delegate.open()

        return

    ###########################################################################
    # 'ShellPlotFrame' interface.
    ###########################################################################

    def get_window_geometry(self):
        """ Get the position and size of the window. """
        
        pass

    def set_window_geometry(self, geometry):
        """ Set the position and size of the window. """
        
        pass

    def is_alive(self):
        """ Get the status of the proxy object. """
        
        return self.proxy_object_alive

    def raise_window(self):
        """ Make the window the topmost window. """
        
        pass

    def close_window(self):
        """ Close the window. """
        
        self.delegate.close()
        
        return

    def destroy_window(self):
        """ Destroy the window. """

        # fixme: The following lines are a hack to force garbage collection:
        # self.dispose_group( self.container.component )
        self._component = self.container = self.delegate = None

        return

    def show_error(self, msg):
        """ Show an error dialog. """
        
        pass

    def make_menu(self, menu_desc):
        """ Create a menu. """

        ## FIXME: We probably need to rethink this wrt pyface menus.
        pass

    def make_plot_container(self, canvas, **traits):
        """ Create the container for the actual plot. """
        
        self._component = PlotComponent(canvas)
        
        return self._component
        

# Hook ourselves in as the provider of plot frames.
import enthought.chaco.plt as base
base.ShellPlotFrame_factory = EditorShellPlotFrame

editor_factory = EditorProxyFrame

#### EOF ######################################################################
    

