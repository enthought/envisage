# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
"""
A base class for editors that can be tracked by single project plugin projects.

"""

# Standard library imports.
import logging

# Enthought library imports
from envisage.workbench import DecoratedEditor
from traits.api import Instance

# Application specific imports.
from envisage.single_project.services import IPROJECT_MODEL


# Setup a logger for this module.
logger=logging.getLogger(__name__)


class ProjectEditor(DecoratedEditor):
    """
    A base class for editors that can be tracked by single project plugin
    projects.

    """

    #########################################################################
    # Attributes
    #########################################################################

    ### public 'ProjectEditor' interface ####################################

    # The project containing the resource we're editing
    project = Instance('envisage.single_project.project.Project')


    #########################################################################
    # `object` interface
    #########################################################################

    #### operator methods ###################################################

    def __init__(self, **traits):
        """
        Constructor.

        Extended to associate ourself with the current project.

        """

        super(ProjectEditor, self).__init__(**traits)

        # Make sure the current project knows this editor is associated with
        # it's resources
        model_service = self.window.application.get_service(IPROJECT_MODEL)
        self.project = model_service.project
        self.project.register_editor(self.resource, self)

        return


    #########################################################################
    # 'Editor' interface.
    #########################################################################

    ### public 'Editor' interface ###########################################

    def destroy_control(self):
        """
        Destroys the toolkit-specific control that represents the editor.

        Extended to ensure that the current project stops associating us
        with its resources.

        """

        # Only do something if the editor is still open
        if self.control:
            logger.debug('Destroying control in ProjectEditor [%s]', self)

            # Unregister from the associated project immediately.
            self.project.register_editor(self.resource, self, remove=True)

        super(ProjectEditor, self).destroy_control()

        return


#### EOF ####################################################################
