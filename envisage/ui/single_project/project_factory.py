# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
"""
A base class for project factories.

"""

# Standard library imports
import logging

# Enthought library imports
from envisage.api import IApplication
from traits.api import HasTraits, Instance

# Local imports.
from .project import Project


# Setup a logger for this module.
logger = logging.getLogger(__name__)


class ProjectFactory(HasTraits):
    """
    A base class for project factories.

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
    PROJECT_CLASS = Project

    # Current envisage application.
    application = Instance(IApplication)


    ##########################################################################
    # 'ProjectFactory' interface.
    ##########################################################################

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


#### EOF #####################################################################

