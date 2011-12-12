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

# Local imports.
from encore.events.event_manager import EventManager


class EventManagerPlugin(Plugin):
    """ Plugin to add event manager to the application. """

    id = 'canopy.event_manager'

    SERVICE_OFFERS = 'envisage.service_offers'
    service_offers = List(contributes_to=SERVICE_OFFERS)

    evt_mgr = Any

    def _service_offers_default(self):
        evt_mgr = self.evt_mgr # Ensure evt_mgr is created
        evt_mgr_service_offer = ServiceOffer(
            protocol   = EventManager,
            factory    = lambda: evt_mgr,
        )
        return [evt_mgr_service_offer]

    def _evt_mgr_default(self):
        """ If application already has an EventManager, then that is returned.
        """
        app = self.application
        evt_mgr = getattr(app, 'evt_mgr', None)
        if evt_mgr is None:
            evt_mgr = EventManager()
            app.evt_mgr = evt_mgr
        return evt_mgr

