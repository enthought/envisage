# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
"""
Envisage GUI Plugin
-------------------

This is a plugin which contributes a Pyface GUI instance to be used in
applications with a desktop UI.  This does not support the splash screen
features of IGUI - those are better controlled by the application or main
script as they generally should be shown as soon as possible after startup,
often before expensive imports or operations.
"""

from traits.api import List, Instance
from envisage.service_offer import ServiceOffer
from envisage.plugin import Plugin
from envisage.ids import SERVICE_OFFERS
from envisage.ui.ids import IGUI_PROTOCOL


class GUIPlugin(Plugin):
    """ A simple plugin that provides a Pyface GUI.

    This class handles the life-cycle of a Pyface GUI.  Applications that need
    the GUI object should request the `pyface.i_gui.IGUI` interface, allowing
    things like alternative event loops (eg. intergation with asyncio).
    """

    #### 'GUIPlugin' interface #########################################

    service_offers = List(contributes_to=SERVICE_OFFERS)

    #: The Pyface GUI for the application.
    _gui = Instance("pyface.i_gui.IGUI")

    #### 'IPlugin' interface ##################################################

    #: The plugin's unique identifier.
    id = "envisage.ui.gui"

    #: The plugin's name (suitable for displaying to the user).
    name = "GUI Plugin"

    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    def stop(self):
        self._destroy_gui()
        super().stop()

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_gui(self):
        if self._gui is None:
            from pyface.gui import GUI

            self._gui = GUI()

        return self._gui

    def _destroy_gui(self):
        if self._gui is not None:
            self._gui = None

    #### Trait initializers ###################################################

    def _service_offers_default(self):
        i_gui_service_offer = ServiceOffer(
            protocol=IGUI_PROTOCOL,
            factory=self._create_gui,
        )
        return [i_gui_service_offer]

    def __gui_default(self):
        from pyface.gui import GUI

        return GUI()
