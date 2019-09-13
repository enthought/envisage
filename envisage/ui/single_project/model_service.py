# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
"""
The Envisage service providing the model state for the single
project plugin.

"""

# Standard imports
import logging
import os
import shutil

# Enthought library imports
from envisage.api import IApplication
from apptools.preferences.api import IPreferences
from traits.api import Any, HasTraits, Instance, List


# Setup a logger for this module.
logger = logging.getLogger(__name__)


class ModelService(HasTraits):
    """
    The Envisage service providing the model state for the single
    project plugin.

    """

    ##########################################################################
    # Attributes (Traits)
    ##########################################################################

    ### public 'ModelService' interface ######################################

    # The Envisage application that this service is part of.
    application = Instance(IApplication)

    # The factory to use for creating new projects
    factory = Instance('envisage.ui.single_project.project_factory.'
        'ProjectFactory')

    # The preferences to be exposed through this service.
    preferences = Instance(IPreferences)

    # The currently open project
    project = Instance('envisage.ui.single_project.project.Project')

    # The current selection within the current project.
    selection = List(Any)


    ##########################################################################
    # 'object' interface.
    ##########################################################################

    ### operator methods #####################################################

    def __init__(self, application, factory, **traits):
        """
        Constructor.

        We require a reference to an Envisage application and a project
        factory to create an instance.

        """

        super(ModelService, self).__init__(application = application,
            factory = factory, **traits)

        return


    ##########################################################################
    # 'ModelService' interface.
    ##########################################################################

    ### public interface #####################################################

    def are_projects_files(self):
        """
        Returns True if project instances are saved as files and False if
        they are saved as directories.

        """

        return self.factory.PROJECT_CLASS.PROJECTS_ARE_FILES


    def clean_location(self, location):
        """
        Ensures that there are no existing files or directories at the
        specified location by removing them.  Exceptions are raised if
        there are any errors cleaning out existing files or directories.

        """

        logger.debug('Trying to clean location [%s]', location)

        if os.path.isfile(location):
            os.path.remove(location)
        else:
            shutil.rmtree(location)

        return


    def get_default_path(self):
        """
        Return the default location for projects.

        """

        return self.factory.PROJECT_CLASS.get_default_path(self.application)


    ### trait handlers #######################################################

    def _project_changed(self, old, new):
        """
        Called whenever the current project is changed.

        We hook this to make sure the new project knows it's current and
        the old project knows it's not.

        """

        logger.debug('Detected project change from [%s] to [%s] in '
            'ModelService [%s]', old, new, self)

        if old is not None:
            old.stop()
        self.selection = []
        if new is not None:
            new.start()

        return


    def _selection_changed(self, old, new):
        """
        Called whenever the selection within the project is changed.

        Implemented simply to log the change.

        """

        logger.debug('ModelService [%s] selection changed from [%s] to [%s] ',
             self, old, new)

        return


### EOF ######################################################################

