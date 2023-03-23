# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Used to track events in tests. """


# Enthought library imports.
from traits.api import HasTraits, List, Str, Tuple
from traits.has_traits import observe


class EventTracker(HasTraits):
    """Used to track traits events."""

    # The traits events that have fired.
    #
    # This is a list of tuples in the form:-
    #
    # (obj, trait_name, old, new)
    events = List(Tuple)

    # The names of the traits events that have fired.
    #
    # This is useful if you just care about the order of the events, not the
    # contents.
    event_names = List(Str)

    # The trait event subscriptions used by the tracker.
    #
    # This is a list of tuples in the form:-
    #
    # (obj, trait_name)
    #
    # Where 'obj' is the object to listen to, and 'trait_name' is the name of
    # the trait to listen to, or None to listen for all trait events.
    subscriptions = List(Tuple)

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handlers ################################################

    @observe("subscriptions")
    def _update_listeners_on_all_subscriptions(self, event):
        """Static trait change handler."""
        old, new = event.old, event.new
        for subscription in old:
            self._remove_subscription(subscription)

        for subscription in new:
            self._add_subscription(subscription)

    @observe("subscriptions:items")
    def _update_listeners_on_changed_subscriptions(self, event):
        """Static trait change handler."""

        for subscription in event.removed:
            self._remove_subscription(subscription)

        for subscription in event.added:
            self._add_subscription(subscription)

    def _listener(self, obj, trait_name, old, new):
        """Dynamic trait change listener."""

        self.events.append((obj, trait_name, old, new))
        self.event_names.append(trait_name)

    #### Methods ##############################################################

    def _add_subscription(self, subscription):
        """Add a subscription."""

        obj, trait_name = subscription

        if trait_name is not None:
            obj.on_trait_change(self._listener, trait_name)

        else:
            obj.on_trait_change(self._listener)

    def _remove_subscription(self, subscription):
        """Remove a subscription."""

        obj, trait_name = subscription

        if trait_name is not None:
            obj.on_trait_change(self._listener, trait_name, remove=True)

        else:
            obj.on_trait_change(self._listener, remove=True)
