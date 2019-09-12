# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" An extensible workbench window. """


# Standard library imports.
import logging

# Enthought library imports.
import pyface.workbench.api as pyface

from envisage.api import IExtensionPointUser, IExtensionRegistry
from envisage.api import IServiceRegistry
from envisage.api import ExtensionPoint, ServiceRegistry
from envisage.ui.action.api import ActionSet
from pyface.action.api import StatusBarManager
from traits.api import Delegate, Instance, List, Property, provides

# Local imports.
from .workbench_action_manager_builder import WorkbenchActionManagerBuilder
from .workbench_editor_manager import WorkbenchEditorManager


# Logging.
logger = logging.getLogger(__name__)


@provides(IServiceRegistry, IExtensionPointUser)
class WorkbenchWindow(pyface.WorkbenchWindow):
    """ An extensible workbench window. """

    # Extension point Ids.
    ACTION_SETS    = 'envisage.ui.workbench.action_sets'
    VIEWS          = 'envisage.ui.workbench.views'
    PERSPECTIVES   = 'envisage.ui.workbench.perspectives'
    SERVICE_OFFERS = 'envisage.ui.workbench.service_offers'

    #### 'WorkbenchWindow' interface ##########################################

    # The application that the window is part of.
    #
    # This is equivalent to 'self.workbench.application', and is provided just
    # as a convenience since windows often want access to the application.
    application = Delegate('workbench', modify=True)

    # The action sets that provide the toolbars, menus groups and actions
    # used in the window.
    action_sets = List(Instance(ActionSet))

    # The service registry for 'per window' services.
    service_registry = Instance(IServiceRegistry, factory=ServiceRegistry)

    #### 'IExtensionPointUser' interface ######################################

    # The extension registry that the object's extension points are stored in.
    extension_registry = Property(Instance(IExtensionRegistry))

    #### Private interface ####################################################

    # The workbench menu and tool bar builder.
    #
    # The builder is used to create the window's tool bar and menu bar by
    # combining all of the contributed action sets.
    _action_manager_builder = Instance(WorkbenchActionManagerBuilder)

    # Contributed action sets (each contribution is actually a factory).
    _action_sets = ExtensionPoint(id=ACTION_SETS)

    # Contributed views (each contribution is actually a factory).
    _views = ExtensionPoint(id=VIEWS)

    # Contributed perspectives (each contribution is actually a factory).
    _perspectives = ExtensionPoint(id=PERSPECTIVES)

    # Contributed service offers.
    _service_offers = ExtensionPoint(id=SERVICE_OFFERS)

    # The Ids of the services that were automatically registered.
    _service_ids = List

    ###########################################################################
    # 'IExtensionPointUser' interface.
    ###########################################################################

    def _get_extension_registry(self):
        """ Trait property getter. """

        return self.application

    ###########################################################################
    # 'pyface.Window' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _menu_bar_manager_default(self):
        """ Trait initializer. """

        return self._action_manager_builder.create_menu_bar_manager('MenuBar')

    def _status_bar_manager_default(self):
        """ Trait initializer. """

        return StatusBarManager()

    def _tool_bar_managers_default(self):
        """ Trait initializer. """

        return self._action_manager_builder.create_tool_bar_managers('ToolBar')

    #### Trait change handlers ################################################

    def _opening_changed(self):
        """ Static trait change handler. """

        self._service_ids = self._register_service_offers(self._service_offers)

        return

    def _closed_changed(self):
        """ Static trait change handler. """

        self._unregister_service_offers(self._service_ids)

        return

    ###########################################################################
    # 'pyface.WorkbenchWindow' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _editor_manager_default(self):
        """ Trait initializer. """

        return WorkbenchEditorManager(window=self)

    def _icon_default(self):
        """ Trait initializer. """

        return self.workbench.application.icon

    def _perspectives_default(self):
        """ Trait initializer. """

        return [factory() for factory in self._perspectives]

    def _title_default(self):
        """ Trait initializer. """

        return self.workbench.application.name

    def _views_default(self):
        """ Trait initializer. """

        return [factory(window=self) for factory in self._views]

    ###########################################################################
    # 'WorkbenchWindow' interface.
    ###########################################################################

    def _action_sets_default(self):
        """ Trait initializer. """

        return [factory(window=self) for factory in self._action_sets]

    ###########################################################################
    # 'IServiceRegistry' interface.
    ###########################################################################

    def get_service(self, protocol, query='', minimize='', maximize=''):
        """ Return at most one service that matches the specified query. """

        service = self.service_registry.get_service(
            protocol, query, minimize, maximize
        )

        return service

    def get_service_properties(self, service_id):
        """ Return the dictionary of properties associated with a service. """

        return self.service_registry.get_service_properties(service_id)

    def get_services(self, protocol, query='', minimize='', maximize=''):
        """ Return all services that match the specified query. """

        services = self.service_registry.get_services(
            protocol, query, minimize, maximize
        )

        return services

    def register_service(self, protocol, obj, properties=None):
        """ Register a service. """

        service_id = self.service_registry.register_service(
            protocol, obj, properties
        )

        return service_id

    def set_service_properties(self, service_id, properties):
        """ Set the dictionary of properties associated with a service. """

        self.service_registry.set_service_properties(service_id, properties)

        return

    def unregister_service(self, service_id):
        """ Unregister a service. """

        self.service_registry.unregister_service(service_id)

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def __action_manager_builder_default(self):
        """ Trait initializer. """

        action_manager_builder = WorkbenchActionManagerBuilder(
            window=self, action_sets=self.action_sets
        )

        return action_manager_builder

    def _register_service_offers(self, service_offers):
        """ Register all service offers. """

        return list(map(self._register_service_offer, service_offers))

    def _register_service_offer(self, service_offer):
        """ Register a service offer. """

        # Add the window to the service offer properties (this is so that it
        # is available to the factory when it is called to create the actual
        # service).
        service_offer.properties['window'] = self

        service_id = self.register_service(
            protocol   = service_offer.protocol,
            obj        = service_offer.factory,
            properties = service_offer.properties
        )

        return service_id

    def _unregister_service_offers(self, service_ids):
        """ Unregister all service offers. """

        # Unregister the services in the reverse order that we registered
        # them.
        service_ids_copy = service_ids[:]
        service_ids_copy.reverse()

        for service_id in service_ids_copy:
            self.unregister_service(service_id)

        return

#### EOF ######################################################################
