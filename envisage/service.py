# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" A trait type used to access services. """


# Standard library imports.
import logging

# Enthought library imports.
from traits.api import TraitError, TraitType

# Logging.
logger = logging.getLogger(__name__)


class Service(TraitType):
    """A trait type used to access services.

    Note that this is a trait *type* and hence does *NOT* have traits itself
    (i.e. it does *not* inherit from 'HasTraits').

    """

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(
        self, protocol=None, query="", minimize="", maximize="", **metadata
    ):
        """Constructor."""

        super().__init__(**metadata)

        # The protocol that the service must provide.
        self._protocol = protocol

        # The optional query.
        self._query = query

        # The optional name of the trait/property to minimize.
        self._minimize = minimize

        # The optional name of the trait/property to maximize.
        self._maximize = maximize

    def __repr__(self):
        """String representation of a Service object"""
        return "Service(protocol={!r})".format(self._protocol)

    ###########################################################################
    # 'TraitType' interface.
    ###########################################################################

    def get(self, obj, trait_name):
        """Trait type getter."""

        service_registry = self._get_service_registry(obj)

        obj = service_registry.get_service(
            self._protocol, self._query, self._minimize, self._maximize
        )

        return obj

    def set(self, obj, name, value):
        """Trait type setter."""

        raise TraitError("Service traits cannot be set")

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_service_registry(self, obj):
        """Return the service registry in effect for an object."""

        service_registry = getattr(obj, "service_registry", None)
        if service_registry is None:
            raise ValueError(
                'The "Service" trait type can only be used within objects '
                "that have a reference to a service registry via their "
                '"service_registry" trait. \n'
                "Object %s\nService protocol %s" % (obj, self._protocol)
            )

        return service_registry
