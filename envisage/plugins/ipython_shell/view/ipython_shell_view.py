""" A view containing an interactive Python shell. """


# Standard library imports.
import logging
import traceback

# Major library imports
from IPython.kernel.core.interpreter import Interpreter

# Enthought library imports.
from envisage.api import IExtensionRegistry
from envisage.api import ExtensionPoint
from envisage.plugins.python_shell.api import IPythonShell
from envisage.plugins.ipython_shell.api import INamespaceView
from pyface.workbench.api import View
from pyface.ipython_widget import IPythonWidget
from pyface.api import GUI
from traits.api import Instance, Property, provides, Dict


# Setup a logger for this module.
logger = logging.getLogger(__name__)

@provides(IPythonShell)
class IPythonShellView(View):
    """ A view containing an IPython shell. """

    #### 'IView' interface ####################################################

    # The part's globally unique identifier.
    id = 'envisage.plugins.python_shell_view'

    # The part's name (displayed to the user).
    name = 'IPython'

    # The default position of the view relative to the item specified in the
    # 'relative_to' trait.
    position = 'bottom'

    #### 'PythonShellView' interface ##########################################

    # The interpreter's namespace.
    namespace = Dict

    # The names bound in the interpreter's namespace.
    names = Property(depends_on="namespace")

    #### 'IPythonShellView' interface #########################################

    # The interpreter
    interpreter = Instance(Interpreter)

    def _interpreter_default(self):
        # Create an interpreter that has a reference to our namespace.
        return Interpreter(user_ns=self.namespace)

    #### 'IExtensionPointUser' interface ######################################

    # The extension registry that the object's extension points are stored in.
    extension_registry = Property(Instance(IExtensionRegistry))

    #### Private interface ####################################################

    # Banner.
    _banner = ExtensionPoint(id='envisage.plugins.ipython_shell.banner')

    # Bindings.
    _bindings = ExtensionPoint(id='envisage.plugins.python_shell.bindings')

    # Commands.
    _commands = ExtensionPoint(id='envisage.plugins.python_shell.commands')

    ###########################################################################
    # 'IExtensionPointUser' interface.
    ###########################################################################

    def _get_extension_registry(self):
        """ Trait property getter. """

        return self.window.application

    ###########################################################################
    # 'View' interface.
    ###########################################################################

    def create_control(self, parent):
        """ Creates the toolkit-specific control that represents the view. """

        self.shell = IPythonWidget(parent,
                                   banner='\n'.join(self._banner),
                                   interp=self.interpreter)

        # Namespace contributions.
        for bindings in self._bindings:
            for name, value in bindings.items():
                self.bind(name, value)

        for command in self._commands:
            try:
                self.execute_command(command)
            except Exception as e:
                logger.exception(
                        "The command '%s' supplied to the Ipython shell "
                        "plugin has raised an exception:\n%s" %
                        (command, traceback.format_exc()))

        # Register the view as a service.
        self.window.application.register_service(IPythonShell, self)

        ns_view = self.window.application.get_service(INamespaceView)
        if ns_view is not None:
            self.on_trait_change(ns_view._on_names_changed, 'names')

        def try_set_focus():
            try:
                self.shell.control.SetFocus()
            except:
                # The window may not have been created yet.
                pass

        def set_focus():
            self.window.application.gui.invoke_later(try_set_focus)

        GUI.invoke_later(set_focus)

        return self.shell.control


    def destroy_control(self):
        """ Destroys the toolkit-specific control that represents the view.

        """

        super(IPythonShellView, self).destroy_control()

        # Remove the namespace change handler
        ns_view = self.window.application.get_service(INamespaceView)
        if ns_view is not None:
            self.on_trait_change(
                ns_view._on_names_changed, 'names', remove=True
            )


    ###########################################################################
    # 'PythonShellView' interface.
    ###########################################################################

    #### Properties ###########################################################

    def _get_names(self):
        """ Property getter. """

        return self.control.ipython0.magic_who_ls()

    #### Methods ##############################################################

    def bind(self, name, value):
        """ Binds a name to a value in the interpreter's namespace. """

        self.namespace[name] = value

        return

    def execute_command(self, command, hidden=True):
        """ Execute a command in the interpreter. """

        self.shell.execute_command(command, hidden)
        self.trait_property_changed('namespace', [], self.namespace)

    def execute_file(self, path, hidden=True):
        """ Execute a command in the interpreter. """

        self.shell.execute_file(path, hidden)
        self.trait_property_changed('namespace', [], self.namespace)

    def lookup(self, name):
        """ Returns the value bound to a name in the interpreter's namespace."""

        return self.namespace[name]

#### EOF ######################################################################
