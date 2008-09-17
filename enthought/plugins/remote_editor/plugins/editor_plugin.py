# Standard library imports
import os
import logging

# Local imports
from enthought.plugins.remote_editor.enshell_client import \
    EnshellClient


class EditorPlugin(EnshellClient):

    # EditorPlugin interface

    def new(self):
        raise NotImplementedError

    def open(self, filename):
        raise NotImplementedError

    def run_file(self, path):
        self.send_command('run_file', path)

    def run_text(self, text):
        self.send_command('run_text', text)

    # Client interface

    self_type = "python_editor"
    other_type = "python_shell"

    def handle_command(self, command, arguments):
        if command == "new":
            self.new()
            return True
        elif command == "open":
            if os.path.exists(arguments):
                self.open(arguments)
            else:
                msg = "EditorPlugin recieved invalid path '%s' for 'open' command"
                logging.warning(msg % arguments)
            return True
        return False
