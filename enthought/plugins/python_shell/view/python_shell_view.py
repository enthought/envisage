""" A view containing an interactive Python shell. """


# Standard library imports.
import logging, sys
from sets import Set

# Enthought library imports.
from enthought.envisage.api import IExtensionPointUser, IExtensionRegistry
from enthought.envisage.api import ExtensionPoint
from enthought.plugins.python_shell.api import IPythonShell
from enthought.pyface.api import PythonShell
from enthought.pyface.workbench.api import View
from enthought.traits.api import Any, Event, Instance, Property, implements


# Setup a logger for this module.
logger = logging.getLogger(__name__)


class PseudoFile ( object ):
    """ Simulates a normal File object.
    """

    def __init__(self, write):
        self.write = write

    def readline(self):
        pass

    def writelines(self, l):
        map(self.write, l)

    def flush(self):
        pass

    def isatty(self):
        return 1


class PythonShellView(View):
    """ A view containing an interactive Python shell. """

    implements(IPythonShell)

    #### 'IView' interface ####################################################

    # The view's name.
    name = 'Python'

    # The default position of the view relative to the item specified in the
    # 'relative_to' trait.
    position = 'bottom'

    #### 'PythonShellView' interface ##########################################

    # The interpreter's namespace.
    namespace = Property

    # The names bound in the interpreter's namespace.
    names = Property

    # Original value for 'sys.stdout':
    original_stdout = Any

    # Stdout text is posted to this event
    stdout_text = Event

    #### 'IExtensionPointUser' interface ######################################

    # The extension registry that the object's extension points are stored in.
    extension_registry = Property(Instance(IExtensionRegistry))

    #### Private interface ####################################################

    # Bindings.
    _bindings = ExtensionPoint(id='enthought.plugins.python_shell.bindings')

    # Commands.
    _commands = ExtensionPoint(id='enthought.plugins.python_shell.commands')

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
        
        self.shell = shell = PythonShell(parent)
        shell.on_trait_change(self._on_key_pressed, 'key_pressed')
        shell.on_trait_change(self._on_command_executed, 'command_executed')

        # Write application standard out to this shell instead of to DOS window
        self.on_trait_change(
            self._on_write_stdout, 'stdout_text', dispatch='ui'
        )
        self.original_stdout = sys.stdout
        sys.stdout = PseudoFile(self._write_stdout)

        # Namespace contributions.
        for bindings in self._bindings:
            for name, value in bindings.items():
                self.bind(name, value)

        for command in self._commands:
            self.execute_command(command)

        # We take note of the starting set of names bound in the interpreter's
        # namespace so that we can show the user what they have added or
        # removed in the namespace view.
        self._names = Set(self.names)

        # Register the view as a service.
        self.window.application.register_service(IPythonShell, self)

        return self.shell.control

    def destroy_control(self):
        """ Destroys the toolkit-specific control that represents the view.

        """
        
        super(PythonShellView, self).destroy_control()

        # Remove the sys.stdout handlers.
        self.on_trait_change(
            self._on_write_stdout, 'stdout_text', remove=True
        )

        # Restore the original stdout.
        sys.stdout = self.original_stdout

        return

    ###########################################################################
    # 'PythonShellView' interface.
    ###########################################################################

    #### Properties ###########################################################

    def _get_namespace(self):
        """ Property getter. """

        return self.shell.interpreter().locals

    def _get_names(self):
        """ Property getter. """

        return self.shell.interpreter().locals.keys()

    #### Methods ##############################################################

    def bind(self, name, value):
        """ Binds a name to a value in the interpreter's namespace. """

        self.shell.bind(name, value)

        return

    def execute_command(self, command, hidden=True):
        """ Execute a command in the interpreter. """

        return self.shell.execute_command(command, hidden)

    def lookup(self, name):
        """ Returns the value bound to a name in the interpreter's namespace.

        """

        return self.shell.interpreter().locals[name]

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _write_stdout(self, text):
        """ Handles text written to stdout. """

        self.stdout_text = text

        return
    
    #### Trait change handlers ################################################

    def _on_command_executed(self, shell):
        """ Dynamic trait change handler. """

        if self.control is not None:
            # Get the names that are now bound in the namespace.
            names = Set(self.names)

            # Find the differences in the namespace caused by the command
            # execution.
            added   = names.difference(self._names)
            removed = self._names.difference(names)

            # Remember the new state of the namespace.
            self._names = names

            # Trait event notification.
            if len(added) > 0 or len(removed) > 0:
                # fixme: We might want to get a tad more granular in the event
                # that we fire!
                self.trait_property_changed('namespace', {}, self.namespace)
                self.trait_property_changed('names', [], self.names)

        return

    def _on_key_pressed(self, event):
        """ Dynamic trait change handler. """

        if event.alt_down and event.key_code == 317:
            zoom = self.shell.control.GetZoom()
            if zoom != 20:
                self.shell.control.SetZoom(zoom+1)

        elif event.alt_down and event.key_code == 319:
            zoom = self.shell.control.GetZoom()
            if zoom != -10:
                self.shell.control.SetZoom(zoom-1)

        return

    def _on_write_stdout(self, text):
        """ Dynamic trait change handler. """
        
        self.shell.control.write(text)

        return
    
#### EOF ######################################################################
