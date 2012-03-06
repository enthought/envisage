#
#
# (C) Copyright 2011 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in LICENSE.txt
#
""" This module provides a plugin which adds an EventManager to application.

If the application does not already have an evt_mgr attribute which is an
instance of EventManager, the plugin creates a new EventManager instance,
creates a service to offer the event manager and sets the evt_mgr instance
of the application to the created event manager.
"""

# Enthought library imports.
from envisage.api import Plugin, ServiceOffer
from traits.api import List, Any


class EventManagerPlugin(Plugin):
    """ Plugin to add event manager to the application. """

    id = 'envisage.event_manager'

    SERVICE_OFFERS = 'envisage.service_offers'
    service_offers = List(contributes_to=SERVICE_OFFERS)

    def _service_offers_default(self):
        from encore.events.api import BaseEventManager, get_event_manager

        evt_mgr_service_offer = ServiceOffer(
            protocol   = BaseEventManager,
            factory    = get_event_manager,
        )
        return [evt_mgr_service_offer]

