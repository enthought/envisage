# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
"""
A base class for actions that determine their enabled status based on
the state of the current project.

"""

# Standard library imports
import logging
import inspect

# Enthought library imports
from envisage.api import Application
from envisage.ui.workbench.api import WorkbenchWindow
from pyface.action.api import Action
from traits.api import Instance, Str

# Local imports.
from envisage.ui.single_project.services import IPROJECT_MODEL


# Setup a logger for this module.
logger = logging.getLogger(__name__)


class ProjectAction(Action):
    """
    A base class for actions that determine their enabled status based on
    the state of the current project.

    This class is architected such that implementors can override the
    'refresh' method without losing the default logic that determines
    the enabled state as a function of the current project.

    """
    #### 'ProjectAction' interface ####################################

    # The application that the action is part of. This is a convenience
    # property and is equivalent to 'self.window.application'.
    application = Instance(Application)

    # The project model service we refresh our state against.
    model_service = Instance(IPROJECT_MODEL)

    # The universal object locator (UOL). This string is used to locate an
    # instance to invoke a method on.
    #
    # UOLs can currently have one of the following forms:
    #
    # * ``'service://a_service_identifier'``
    # * ``'name://a/path/through/the/naming/service'``
    # * ``'file://the/pathname/of/a/file/containing/a/UOL'``
    # * ``'http://a/URL/pointing/to/a/text/document/containing/a/UOL'``
    uol = Str

    # The name of the method to invoke on the object.
    method_name = Str

    ##########################################################################
    # 'object' interface
    ##########################################################################

    def __init__(self, *args, **kws):
        """
        Constructor.

        Extended to setup a listener on the project model service so
        that we can refresh whenever the project changes.

        """

        # Retrieve the project model service and register ourself to listen
        # for project state changes.  This is done first to avoid errors
        # during any refresh calls triggered by further initialization.
        # FIXME: I don't think my implementation of the ProjectAction class is correct
        # because I can't see to get a reference to the current application.  Because of
        # this, I'm not able to setup the listeners yet but this needs to be done eventually!
        """
        if 'model_service' in kws:
            self.model_service = kws['model_service']
            del kws['model_service']
        else:
            self.model_service = self.window.application.get_service(IPROJECT_MODEL)
        self._update_model_service_listeners(remove=False)
        """

        super(ProjectAction, self).__init__(*args, **kws)

        return

    ##########################################################################
    # 'Action' interface
    ##########################################################################

    #### public interface ####################################################

    def destroy(self):
        """
        Destroy this action.

        Overridden here to remove our project model service listeners.

        """

        self._update_model_service_listeners(remove=True)

        return

    ##########################################################################
    # 'ProjectAction' interface
    ##########################################################################

    #### public interface ####################################################

    def refresh(self):
        """
        Refresh the enabled state of this action.

        This default implementation enables the action only when there is a
        current project.

        """

        self.enabled = self._refresh_project_exists()

        return

    def perform(self, event):
        """ Performs the action.

        This implementation simply performs the action specified by **uol**
        and **method_name**.

        Override this method to add additional work to the performance of this
        action.

        """

        self._perform_uol_action(event)

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _perform_uol_action(self, event):
        """ Called to perform the configured UOL action. """

        # Find the object.
        object = event.window.application.get_service(self.uol)
        if object is not None:
            method = getattr(object, self.method_name)

            # If the only argument is 'self' then don't pass the event. This
            # makes it easier to hook up actions that invoke NON-UI methods.
            #
            # fixme: Should we check the argument spec of the method more
            # closely and only pass the event iff there is exactly one argument
            # called 'event'?
            args, varargs, varkw, dflts = inspect.getargspec(method)
            if len(args) == 1:
                method()

            else:
                method(event)

        else:
            logger.error("Cannot resolve UOL: %s" % self.uol)

        return


    #### protected interface #################################################

    def _refresh_project_exists(self):
        """
        Return the refresh state according to whether the model service has a
        current project.

        Returns True if this action should be enabled.  False otherwise.

        """

        enabled = False
        if self.model_service is not None \
            and self.model_service.project is not None:
            enabled = True

        return enabled


    def _update_model_service_listeners(self, remove=False):
        """
        Update our listeners on the project model service.

        These are done as individual listener methods so that derived
        classes can change the behavior when a single event occurs.

        """

        logger.debug( (remove and 'Removing ' or 'Adding ') + \
            'listeners on project model service for ProjectAction [%s]', self)

        self.model_service.on_trait_change(self._on_project_changed,
            'project', remove=remove)
        self.model_service.on_trait_change(self._on_project_selection_changed,
            'selection', remove=remove)

        return


    #### trait handlers ######################################################

    def _on_project_changed(self, obj, trait_name, old, new):
        """
        Handle changes to the value of the current project.

        """

        self.refresh()

        return


    def _on_project_selection_changed(self, obj, trait_name, old, new):
        """
        Handle changes to the selection value within the current project.

        """

        self.refresh()

        return


#### EOF #####################################################################
