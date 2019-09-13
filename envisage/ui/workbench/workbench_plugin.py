# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" The Envisage workbench plugin. """


# Enthought library imports.
from envisage.api import ExtensionPoint, Plugin, ServiceOffer
from traits.api import Callable, List


# This module's package.
PKG = '.'.join(__name__.split('.')[:-1])


class WorkbenchPlugin(Plugin):
    """ The Envisage workbench plugin.

    The workbench plugin uses the Pyface workbench to provide the basis of an
    IDE-like user interface. The interface is made up of perspectives, views
    and editors.

    Note that this is not intended to be a 'general-purpose' plugin for user
    interfaces - it provides an IDE-like style and that is all. If your
    application requires another style of interface then write another plugin
    (you can still re-use all the menu, group and action contribution stuff!).

    """

    # The Ids of the extension points that this plugin offers.
    ACTION_SETS              = PKG + '.action_sets'
    PERSPECTIVES             = PKG + '.perspectives'
    PREFERENCES_PAGES        = PKG + '.preferences_pages'
    WORKBENCH_SERVICE_OFFERS = PKG + '.service_offers'
    VIEWS                    = PKG + '.views'

    # The Ids of the extension points that this plugin contributes to.
    PREFERENCES    = 'envisage.preferences'
    SERVICE_OFFERS = 'envisage.service_offers'

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'envisage.ui.workbench'

    # The plugin's name (suitable for displaying to the user).
    name = 'Workbench'

    #### Extension points offered by this plugin ##############################

    action_sets = ExtensionPoint(
        List(Callable), id=ACTION_SETS, desc="""

        An action set contains the toobars, menus, groups and actions that you
        would like to add to top-level workbench windows (i.e. the main
        application window). You can create new toolbars, menus and groups
        and/or add to existing ones.

        Each contribution to this extension point must be a factory that
        creates an action set, where 'factory' means any callable with the
        following signature::

          callable(**traits) -> IActionSet

        The easiest way to contribute such a factory is to create a class
        that derives from 'envisage.ui.action.api.ActionSet'.

        """
    )

    perspectives = ExtensionPoint(
        List(Callable), id=PERSPECTIVES, desc="""

        A perspective is simply an arrangment of views around the (optionally
        hidden) editor area.

        Each contribution to this extension point must be a factory that
        creates a perspective, where 'factory' means any callable with the
        following signature::

          callable(**traits) -> IPerspective

        The easiest way to contribute such a factory is to create a class
        that derives from 'pyface.workbench.api.IPerspective'.

        """
    )

    preferences_pages = ExtensionPoint(
        List(Callable), id=PREFERENCES_PAGES, desc="""

        A preferences page appears in the preferences dialog to allow the user
        to manipulate some preference values.

        Each contribution to this extension point must be a factory that
        creates a preferences page, where 'factory' means any callable with the
        following signature::

          callable(**traits) -> IPreferencesPage

        The easiest way to contribute such a factory is to create a class
        that derives from 'apptools.preferences.ui.api.IPreferencesPage'.

        """
    )

    service_offers = ExtensionPoint(
        List(ServiceOffer),
        id   = WORKBENCH_SERVICE_OFFERS,
        desc = """

        Services are simply objects that a plugin wants to make available to
        other plugins. This extension point allows you to offer 'per
        window' services that are created 'on-demand' (where 'on demand' means
        the first time somebody looks up a service of the appropriate
        protocol).
        .

        e.g.

        my_service_offer = ServiceOffer(
            protocol   = 'acme.IMyService',
            factory    = an_object_or_a_callable_that_creates_one,
            properties = {'a dictionary' : 'that is passed to the factory'}
        )

        Any properties specified are passed as keywrod arguments to the
        factory, i.e. the factory signature is::

          callable(**properties)

        """
    )

    views = ExtensionPoint(
        List(Callable), id=VIEWS, desc="""

        A view provides information to the user to support their current
        task. Views can contain anything you like(!) and are arranged around
        the (optionally hidden) editor area. The user can re-arrange views as
        he/she sees fit.

        Each contribution to this extension point must be a factory that
        creates a view, where 'factory' means any callable with the following
        signature::

          callable(**traits) -> IView

        The easiest way to contribute such a factory is to create a class
        that derives from 'pyface.workbench.api.View'.

        It is also common to use a simple function (especially when a view
        is a representation of a service) e.g::

            def foo_view_factory(**traits):
                ' Create a view that is a representation of a service. '
                foo = self.application.get_service('IFoo')

                return FooView(foo=foo, **traits)

        """
    )

    #### Contributions to extension points made by this plugin ################

    my_action_sets = List(contributes_to=ACTION_SETS)

    def _my_action_sets_default(self):
        """ Trait initializer. """

        from .default_action_set import DefaultActionSet

        return [DefaultActionSet]

    my_preferences = List(contributes_to=PREFERENCES)

    def _my_preferences_default(self):
        """ Trait initializer. """

        return ['pkgfile://envisage.ui.workbench/preferences.ini']

    my_preferences_pages = List(contributes_to=PREFERENCES_PAGES)

    def _my_preferences_pages_default(self):
        """ Trait initializer. """

        from .workbench_preferences_page import WorkbenchPreferencesPage

        return [WorkbenchPreferencesPage]

    my_service_offers = List(contributes_to=SERVICE_OFFERS)

    def _my_service_offers_default(self):
        """ Trait initializer. """

        preferences_manager_service_offer = ServiceOffer(
            protocol = 'apptools.preferences.ui.preferences_manager'
                       '.PreferencesManager',
            factory  = self._create_preferences_manager_service
        )

        workbench_service_offer = ServiceOffer(
            protocol = 'envisage.ui.workbench.workbench.Workbench',
            factory  = self._create_workbench_service
        )

        return [preferences_manager_service_offer, workbench_service_offer]

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_preferences_manager_service(self, **properties):
        """ Factory method for the preferences manager service. """

        from apptools.preferences.ui.api import PreferencesManager

        preferences_manager = PreferencesManager(
            pages=[factory() for factory in self.preferences_pages]
        )

        return preferences_manager

    def _create_workbench_service(self, **properties):
        """ Factory method for the workbench service. """

        # We don't actually create the workbench here, we just return a
        # reference to it.
        #
        # fixme: This guard is really just for testing when we have the
        # workbench plugin as a source egg (i.e. if the egg is on our path
        # then we get the plugin for any egg-based application, even if it is
        # not a workbench application!).
        return getattr(self.application, 'workbench', None)

### EOF ######################################################################
