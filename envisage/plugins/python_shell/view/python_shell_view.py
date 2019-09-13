# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" A view containing an interactive Python shell. """


# Standard library imports.
import logging, sys

# Enthought library imports.
from envisage.api import IExtensionRegistry
from envisage.api import ExtensionPoint
from envisage.plugins.python_shell.api import IPythonShell
from pyface.api import PythonShell
from pyface.workbench.api import View
from traits.api import Any, Event, Instance, Property, DictStrAny, provides

# Setup a logger for this module.
logger = logging.getLogger(__name__)


class PseudoFile ( object ):
    """ Simulates a normal File object.
    """

    def __init__(self, write):
        self.write = write

    def readline(self):
        pass

    def writelines(self, lines):
        for line in lines:
            self.write(line)

    def flush(self):
        pass

    def isatty(self):
        return 1


@provides(IPythonShell)
class PythonShellView(View):
    """ A view containing an interactive Python shell. """

    #### 'IView' interface ####################################################

    # The part's globally unique identifier.
    id = 'envisage.plugins.python_shell_view'

    # The part's name (displayed to the user).
    name = 'Python'

    # The default position of the view relative to the item specified in the
    # 'relative_to' trait.
    position = 'bottom'

    #### 'PythonShellView' interface ##########################################

    # The interpreter's namespace.
    namespace = Property(DictStrAny)

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

        # We take note of the starting set of names and types bound in the
        # interpreter's namespace so that we can show the user what they have
        # added or removed in the namespace view.
        self._namespace_types = set((name, type(value)) for name, value in \
                                        self.namespace.items())

        # Register the view as a service.
        app = self.window.application
        self._service_id = app.register_service(IPythonShell, self)

        return self.shell.control

    def destroy_control(self):
        """ Destroys the toolkit-specific control that represents the view.

        """

        super(PythonShellView, self).destroy_control()

        # Unregister the view as a service.
        self.window.application.unregister_service(self._service_id)

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

        return list(self.shell.interpreter().locals.keys())

    #### Methods ##############################################################

    def bind(self, name, value):
        """ Binds a name to a value in the interpreter's namespace. """

        self.shell.bind(name, value)

        return

    def execute_command(self, command, hidden=True):
        """ Execute a command in the interpreter. """

        return self.shell.execute_command(command, hidden)

    def execute_file(self, path, hidden=True):
        """ Execute a command in the interpreter. """

        return self.shell.execute_file(path, hidden)

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
            # Get the set of tuples of names and types in the current namespace.
            namespace_types = set((name, type(value)) for name, value in \
                                                        self.namespace.items())
            # Figure out the changes in the namespace, if any.
            added = namespace_types.difference(self._namespace_types)
            removed = self._namespace_types.difference(namespace_types)
            # Cache the new list, to use for comparison next time.
            self._namespace_types = namespace_types
            # Fire events if there are change.
            if len(added) > 0 or len(removed) > 0:
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
