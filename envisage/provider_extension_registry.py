# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" An extension registry implementation with multiple providers. """


# Standard library imports.
import logging

# Enthought library imports.
from traits.api import List, provides, on_trait_change

# Local imports.
from .extension_registry import ExtensionRegistry
from .i_extension_provider import IExtensionProvider
from .i_provider_extension_registry import IProviderExtensionRegistry


# Logging.
logger = logging.getLogger(__name__)


@provides(IProviderExtensionRegistry)
class ProviderExtensionRegistry(ExtensionRegistry):
    """ An extension registry implementation with multiple providers. """

    #### Protected 'ProviderExtensionRegistry' interface ######################

    # The extension providers that populate the registry.
    _providers = List(IExtensionProvider)

    ###########################################################################
    # 'IExtensionRegistry' interface.
    ###########################################################################

    def set_extensions(self, extension_point_id, extensions):
        """ Set the extensions to an extension point. """

        raise SystemError('extension points cannot be set')

    ###########################################################################
    # 'ProviderExtensionRegistry' interface.
    ###########################################################################

    def add_provider(self, provider):
        """ Add an extension provider. """

        events = self._add_provider(provider)

        for extension_point_id, (refs, added, index) in events.items():
            self._call_listeners(refs, extension_point_id, added, [], index)

        return

    def get_providers(self):
        """ Return all of the providers in the registry. """

        return self._providers[:]

    def remove_provider(self, provider):
        """ Remove an extension provider.

        Raise a 'ValueError' if the provider is not in the registry.

        """

        events = self._remove_provider(provider)

        for extension_point_id, (refs, removed, index) in events.items():
            self._call_listeners(refs, extension_point_id, [], removed, index)

        return

    ###########################################################################
    # Protected 'ExtensionRegistry' interface.
    ###########################################################################

    def _get_extensions(self, extension_point_id):
        """ Return the extensions for the given extension point. """

        # If we don't know about the extension point then it sure ain't got
        # any extensions!
        if not extension_point_id in self._extension_points:
            logger.warning(
                'getting extensions of unknown extension point <%s>' \
                % extension_point_id
            )
            extensions = []

        # Has this extension point already been accessed?
        elif extension_point_id in self._extensions:
            extensions = self._extensions[extension_point_id]

        # If not, then ask each provider for its contributions to the extension
        # point.
        else:
            extensions = self._initialize_extensions(extension_point_id)
            self._extensions[extension_point_id] = extensions

        # We store the extensions as a list of lists, with each inner list
        # containing the contributions from a single provider. Here we just
        # concatenate them into a single list.
        #
        # You could use a list comprehension, here:-
        #
        #     all = [x for y in extensions for x in y]
        #
        # But I'm sure that that makes it any clearer ;^)

        all = []
        for extensions_of_single_provider in extensions:
            all.extend(extensions_of_single_provider)
        return all

    ###########################################################################
    # Protected 'ProviderExtensionRegistry' interface.
    ###########################################################################

    def _add_provider(self, provider):
        """ Add a new provider. """

        # Add the provider's extension points.
        self._add_provider_extension_points(provider)

        # Add the provider's extensions.
        events = self._add_provider_extensions(provider)

        # And finally, tag it into the list of providers.
        self._providers.append(provider)

        return events

    def _add_provider_extensions(self, provider):
        """ Add a provider's extensions to the registry. """

        # Each provider can contribute to multiple extension points, so we
        # build up a dictionary of the 'ExtensionPointChanged' events that we
        # need to fire.
        events = {}

        # Does the provider contribute any extensions to an extension point
        # that has already been accessed?

        for extension_point_id, extensions in self._extensions.items():
            new = provider.get_extensions(extension_point_id)

            # We only need fire an event for this extension point if the
            # provider contributes any extensions.
            if len(new) > 0:
                index = sum(map(len, extensions))
                refs  = self._get_listener_refs(extension_point_id)
                events[extension_point_id] = (refs, new[:], index)

            extensions.append(new)

        return events

    def _add_provider_extension_points(self, provider):
        """ Add a provider's extension points to the registry. """

        for extension_point in provider.get_extension_points():
            self._extension_points[extension_point.id] = extension_point

        return

    def _remove_provider(self, provider):
        """ Remove a provider. """

        # Remove the provider's extensions.
        events = self._remove_provider_extensions(provider)

        # Remove the provider's extension points.
        self._remove_provider_extension_points(provider, events)

        # And finally take it out of the list of providers.
        self._providers.remove(provider)

        return events

    def _remove_provider_extensions(self, provider):
        """ Remove a provider's extensions from the registry. """

        # Each provider can contribute to multiple extension points, so we
        # build up a dictionary of the 'ExtensionPointChanged' events that we
        # need to fire.
        events = {}

        # Find the index of the provider in the provider list. Its
        # contributions are at the same index in the extensions list of lists.
        index = self._providers.index(provider)

        # Does the provider contribute any extensions to an extension point
        # that has already been accessed?
        for extension_point_id, extensions in self._extensions.items():
            old = extensions[index]

            # We only need fire an event for this extension point if the
            # provider contributed any extensions.
            if len(old) > 0:
                offset = sum(map(len, extensions[:index]))
                refs  = self._get_listener_refs(extension_point_id)
                events[extension_point_id] = (refs, old[:], offset)

            del extensions[index]

        return events

    def _remove_provider_extension_points(self, provider, events):
        """ Remove a provider's extension points from the registry. """

        for extension_point in provider.get_extension_points():
            # Remove the extension point.
            del self._extension_points[extension_point.id]

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handlers ################################################

    @on_trait_change('_providers:extension_point_changed')
    def _providers_extension_point_changed(self, obj, trait_name, old, event):
        """ Dynamic trait change handler. """

        logger.debug('provider <%s> extension point changed', obj)

        extension_point_id = event.extension_point_id

        # If the extension point has not yet been accessed then we don't fire a
        # changed event.
        #
        # This is because we only access extension points lazily and so we
        # can't tell what has actually changed because we have nothing to
        # compare it to!
        if not extension_point_id in self._extensions:
            return

        # This is a list of lists where each inner list contains the
        # contributions made to the extension point by a single provider.
        #
        # fixme: This causes a problem if the extension point has not yet been
        # accessed! The tricky thing is that if it hasn't been accessed yet
        # how do we know what has changed?!? Maybe we should just return an
        # empty list instead of barfing!
        extensions = self._extensions[extension_point_id]

        # Find the index of the provider in the provider list. Its
        # contributions are at the same index in the extensions list of lists.
        provider_index = self._providers.index(obj)

        # Get the updated list from the provider.
        extensions[provider_index] = obj.get_extensions(extension_point_id)

        # Find where the provider's contributions are in the whole 'list'.
        offset = sum(map(len, extensions[:provider_index]))

        # Translate the event index from one that refers to the list of
        # contributions from the provider, to the list of contributions from
        # all providers.
        index = self._translate_index(event.index, offset)

        # Find out who is listening.
        refs = self._get_listener_refs(extension_point_id)

        # Let any listeners know that the extensions have been added.
        self._call_listeners(
            refs, extension_point_id, event.added, event.removed, index
        )

        return

    #### Methods ##############################################################

    def _initialize_extensions(self, extension_point_id):
        """ Initialize the extensions to an extension point. """

        # We store the extensions as a list of lists, with each inner list
        # containing the contributions from a single provider.
        extensions = []
        for provider in self._providers:
            extensions.append(provider.get_extensions(extension_point_id)[:])

        logger.debug('extensions to <%s> <%s>', extension_point_id, extensions)

        return extensions

    def _translate_index(self, index, offset):
        """ Translate an event index by the given offset. """

        if isinstance(index, slice):
            index = slice(index.start+offset, index.stop+offset, index.step)

        else:
            index = index + offset

        return index

#### EOF ######################################################################
