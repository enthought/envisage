#-----------------------------------------------------------------------------
#
#  Copyright (c) 2006-2007 by Enthought, Inc.
#  All rights reserved.
#
#  Author: Dave Peterson <dpeterson@enthought.com>
#
#-----------------------------------------------------------------------------

"""
A runnable that restores the last opened project.

"""

# Standard library imports
import logging

# Enthought library imports.
from envisage import Runnable
from envisage.workbench.services import IWORKBENCH
from pyface.api import information

# Application imports
from .services import IPROJECT_MODEL, IPROJECT_UI


# Setup a logger for this module.
logger = logging.getLogger(__name__)


class ProjectRunnable(Runnable):
    """
    A runnable that restores the last opened project.

    """

    ##########################################################################
    # 'Runnable' interface.
    ##########################################################################

    #### public interface ####################################################

    def run(self, application):
        """
        Run this runnable.

        Overridden here to: (a) ensure the UI service monitors for the
        closing of the application, and (b) restore the last opened
        project.

        """

        # Ensure our UI service is listening for the application to close.
        # FIXME: This ugly hack (doing this here) is necessary only because
        # this plugin contributes to the workbench plugin and that means the
        # workbench insists on starting us first which means our UI service
        # can't directly reference the workbench service until after
        # everything has been started.
        ui_service = application.get_service(IPROJECT_UI)
        ui_service.listen_for_application_exit()

        # Load the project we were using when we last shutdown.
        model_service = application.get_service(IPROJECT_MODEL)
        location = model_service.preferences.get('project location',
            default=None)
        if location and len(location) > 0:
            logger.info("Opening last project from location [%s]", location)

            try:
                project = model_service.factory.open(location)
            except:
                logger.exception('Error during opening of last project.')
                project = None

            if project is not None:
                model_service.project = project
            else:
                information(self._get_parent_window(application),
                    'Unable to open last project from location:\t\n'
                    '\t%s\n'  % (location) + '\n\n'
                    'The project may no longer exist.',
                    'Can Not Open Last Project',
                    )

        else:
            logger.info('No previous project to open')

        return


    #### protected interface ################################################

    def _get_parent_window(self, application):
        """
        Find and return a reference to the application window.

        If one can not be found, then 'None' is returned.

        """

        window = None
        try:
            workbench = application.get_service(IWORKBENCH)
            window = workbench.active_window.control
        except:
            logger.warn('Unable to retrieve application window reference.')

        return window


#### EOF ######################################################################

