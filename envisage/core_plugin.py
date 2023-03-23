# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The Envisage core plugin. """

from contextlib import closing

from traits.api import List, on_trait_change, Str

# Enthought library imports.
from envisage.extension_point import ExtensionPoint
from envisage.plugin import Plugin
from envisage.service_offer import ServiceOffer


class CorePlugin(Plugin):
    """The Envisage core plugin.

    The core plugin offers facilities that are generally useful when building
    extensible applications such as adapters and hooks etc. It does
    not contain anything to do with user interfaces!

    The core plugin should be started before any other plugin. It is up to
    the plugin manager to do this.

    """

    #: Extension point ID for preferences
    PREFERENCES = "envisage.preferences"

    #: Extension point ID for service offers
    SERVICE_OFFERS = "envisage.service_offers"

    #### 'IPlugin' interface ##################################################

    #: The plugin's unique identifier.
    id = "envisage.core"

    #: The plugin's name (suitable for displaying to the user).
    name = "Core"

    #### Extension points offered by this plugin ##############################

    #: preferences ExtensionPoint
    preferences = ExtensionPoint(
        List(Str),
        id=PREFERENCES,
        desc="""

        Preferences files allow plugins to contribute default values for
        user preferences. Each contributed string must be the URL of a
        file-like object that contains preferences values.

        e.g.

        'pkgfile://envisage/preferences.ini'

        - this looks for the 'preferences.ini' file in the 'envisage'
        package.

        'file://C:/tmp/preferences.ini'

        - this looks for the 'preferences.ini' file in 'C:/tmp'

        'http://some.website/preferences.ini'

        - this looks for the 'preferences.ini' document on the 'some.website'
        web site!

        The files themselves are parsed using the excellent 'ConfigObj'
        package. For detailed documentation please go to:-

        http://www.voidspace.org.uk/python/configobj.html

        """,
    )

    @on_trait_change("preferences_items")
    def _update_preferences(self, event):
        """React to new preferencess being *added*.

        Note that we don't currently do anything if preferences are *removed*.

        """

        self._load_preferences(event.added)

    #: service offers ExtensionPoint
    service_offers = ExtensionPoint(
        List(ServiceOffer),
        id=SERVICE_OFFERS,
        desc="""

        Services are simply objects that a plugin wants to make available to
        other plugins. This extension point allows you to offer services
        that are created 'on-demand'.

        e.g.

        my_service_offer = ServiceOffer(
            protocol   = 'acme.IMyService',
            factory    = an_object_or_a_callable_that_creates_one,
            properties = {'a dictionary' : 'that is passed to the factory'}
        )

        See the documentation for 'ServiceOffer' for more details.

        """,
    )

    @on_trait_change("service_offers_items")
    def _register_new_services(self, event):
        """React to new service offers being *added*.

        Note that we don't currently do anything if services are *removed* as
        we have no facility to let users of the service know that the offer
        has been retracted.

        """
        for service in event.added:
            self._register_service_offer(service)

    #### Contributions to extension points made by this plugin ################

    # None.

    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    def start(self):
        """Start the plugin."""
        # Load all contributed preferences files into the application's root
        # preferences node.
        self._load_preferences(self.preferences)

        # Register all service offers.
        #
        # These services are unregistered by the default plugin activation
        # strategy (due to the fact that we store the service ids in this
        # specific trait!).
        self._service_ids = self._register_service_offers(self.service_offers)

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _load_preferences(self, preferences):
        """Load all contributed preferences into a preferences node."""

        # Enthought library imports.
        from envisage.resource.api import ResourceManager

        # We add the plugin preferences to the default scope. The default scope
        # is a transient scope which means that (quite nicely ;^) we never
        # save the actual default plugin preference values. They will only get
        # saved if a value has been set in another (persistent) scope - which
        # is exactly what happens in the preferences UI.
        default = self.application.preferences.node("default/")

        # The resource manager is used to find the preferences files.
        resource_manager = ResourceManager()
        for resource_name in preferences:
            with closing(resource_manager.file(resource_name)) as f:
                default.load(f)

    def _register_service_offers(self, service_offers):
        """Register a list of service offers."""

        return list(map(self._register_service_offer, service_offers))

    def _register_service_offer(self, service_offer):
        """Register a service offer."""

        service_id = self.application.register_service(
            protocol=service_offer.protocol,
            obj=service_offer.factory,
            properties=service_offer.properties,
        )

        return service_id
