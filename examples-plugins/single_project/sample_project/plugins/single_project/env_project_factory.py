#-----------------------------------------------------------------------------
#
#  Copyright (c) 2007 by Enthought, Inc.
#  All rights reserved.
#
#-----------------------------------------------------------------------------

"""
A customization of the single project factory to make EnvProjects.

"""

# Standard library imports
import logging

# Enthought library imports.
from envisage.api import IApplication
from traits.api import Instance
from envisage.ui.single_project.api import ProjectFactory

# Application imports.
from plugins.single_project.env_project import EnvProject

# Setup a logger for this module.
logger = logging.getLogger(__name__)


class EnvProjectFactory(ProjectFactory):
    """
    A customization of the single project factory to make EnvProjects.

    """

    ##########################################################################
    # Attributes
    ##########################################################################

    #### public 'ProjectFactory' interface ###################################

    # The class of the project created by this factory.
    #
    # This is provided so that the single_project services can call class
    # methods.
    #
    # This value is meant to be constant for the lifetime of this class!
    PROJECT_CLASS = EnvProject

    # Current envisage application.
    application = Instance(IApplication)

    #### public method #######################################################

    def create(self):
        """
        Create a new project from scratch.

        This must return an instance of a Project or 'None'.  A return
        value of 'None' indicates that no project could be created.  The
        plugin will display the default traits view to the user so that
        they can configure this new project.

        """

        return self.PROJECT_CLASS(application=self.application)


    def open(self, location):
        """
        Open a project from the specified location.

        This must return an instance of a Project or 'None'.  A return
        value of 'None' indicates that no project could be opened from
        the specified location.

        """

        try:
            project = self.PROJECT_CLASS.load(location, self.application)
        except:
            logger.exception('Unable to load Project from location %s',
                location)
            project = None

        return project

### EOF ########################################################################
