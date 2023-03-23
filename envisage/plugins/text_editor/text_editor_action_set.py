# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from envisage.ui.action.api import Action, ActionSet, Group


class TextEditorActionSet(ActionSet):
    """The default action set for the Text Editor plugin."""

    groups = [
        Group(id="TextFileGroup", path="MenuBar/File", before="ExitGroup")
    ]

    actions = [
        Action(
            id="NewFileAction",
            name="New Text File",
            class_name="envisage.plugins.text_editor.actions.NewFileAction",
            group="TextFileGroup",
            path="MenuBar/File",
        ),
        Action(
            id="OpenFile",
            name="Open Text File...",
            class_name="envisage.plugins.text_editor.actions.OpenFileAction",
            group="TextFileGroup",
            path="MenuBar/File",
        ),
    ]
