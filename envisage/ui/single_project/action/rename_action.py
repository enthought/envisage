# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" An action that renames an item in the project tree. """


# Enthought library imports.
from envisage.ui.single_project.project_action import ProjectAction


class RenameAction(ProjectAction):
    """ Renames an item in the project tree. """

    #### 'Action' interface ###################################################

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'Rename'

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform (self, event):
        """ Performs the action. """

        event.widget.edit_label(event.node)

        return

    # fixme: This should be a selection listener action that probably is only
    # enabled if there is exactly ONE item in the selection and it is editable.
##     ###########################################################################
##     # 'Action' interface.
##     ###########################################################################

##     def refresh(self):
##         """ Refresh the enabled/disabled state of the action etc.

##         This is called whenever the workbench window that the action is in
##         and/or the selection in that window have been changed.

##         """

##         resource_manager = self.window.application.get_service(
##             'envisage.resource.IResourceManager'
##         )

##         # fixme: It seems there is a glitch in the tree selection handling.
##         # When the selection changes we get an empty selection first, then
##         # the new selection.
##         if len(self.window.selection) > 0:
##             for node in self.window.selection:
##                 resource_type = resource_manager.get_type_of(node.obj)
##                 if resource_type is None or resource_type.node_type is None:
##                     self.enabled = False
##                     break

##                 if not resource_type.node_type.is_editable(node.obj):
##                     self.enabled = False
##                     break

##             else:
##                 self.enabled = True

##         return

#### EOF ######################################################################
