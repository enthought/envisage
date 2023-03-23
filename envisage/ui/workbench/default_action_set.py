# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The default workbench action set. """


# Enthought library imports.
from envisage.ui.action.api import Action, ActionSet, Group, Menu

# This module's package.
PKG = ".".join(__name__.split(".")[:-1])


class DefaultActionSet(ActionSet):
    """The default workbench action set."""

    menus = [
        Menu(
            name="&File",
            path="MenuBar",
            groups=[
                Group(id="OpenGroup"),
                Group(id="SaveGroup"),
                Group(id="ImportGroup"),
                Group(id="ExitGroup"),
            ],
        ),
        Menu(
            path="MenuBar",
            class_name="pyface.workbench.action.api:ViewMenuManager",
        ),
        Menu(
            name="&Tools",
            path="MenuBar",
            groups=[Group(id="PreferencesGroup")],
        ),
        Menu(name="&Help", path="MenuBar", groups=[Group(id="AboutGroup")]),
    ]

    actions = [
        Action(
            path="MenuBar/File",
            group="ExitGroup",
            class_name=PKG + ".action.api:ExitAction",
        ),
        Action(
            path="MenuBar/Tools",
            group="PreferencesGroup",
            class_name=PKG + ".action.api:EditPreferencesAction",
        ),
        Action(
            path="MenuBar/Help",
            group="AboutGroup",
            class_name=PKG + ".action.api:AboutAction",
        ),
    ]
