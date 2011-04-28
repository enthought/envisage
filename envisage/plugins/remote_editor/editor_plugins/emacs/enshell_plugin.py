"""
"""

# System library imports
from Pymacs import lisp

# ETS imports
from envisage.plugins.remote_editor.plugins.editor_plugin import \
        EditorPlugin


client = EditorPlugin()
client.register()

def run_text():
    start = lisp.point()
    end = lisp.mark(True)
    if start > end:
        start, end = end, start
    text = lisp.buffer_substring(start, end)
    if len(text):
        client.run_text(text)
    else:
        # TODO Complain in message bar
        pass

def run_file():
    path = lisp.buffer_file_name()
    if path is None:
        # TODO Complain in message bar
        pass
    else:
        client.run_file(path)
