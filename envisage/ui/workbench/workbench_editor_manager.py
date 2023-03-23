# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" An editor manager that uses contributed editors. """

# Enthought library imports.
from pyface.workbench.api import EditorManager, TraitsUIEditor


class WorkbenchEditorManager(EditorManager):
    """An editor manager that uses contributed editors."""

    ###########################################################################
    # 'IEditorManager' interface.
    ###########################################################################

    def create_editor(self, window, obj, kind):
        """Create an editor for an object.

        For now, the 'kind' is actually a factory that produces editors. It
        should be a callable with the following signature::

            callable(window=window, obj=obj) -> IEditor
        """

        if kind is None:
            kind = TraitsUIEditor

        editor = kind(window=window, obj=obj)

        self.add_editor(editor, kind)

        return editor

    ###########################################################################
    # 'Protected' 'EditorManager'  interface.
    ###########################################################################

    def _is_editing(self, editor, obj, kind):
        """Return True if the editor is editing the object."""

        if kind is None:
            kind = TraitsUIEditor
        return self.get_editor_kind(editor) is kind and editor.obj == obj
