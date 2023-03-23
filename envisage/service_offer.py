# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" An offer to provide a service. """


# Enthought library imports.
from traits.api import Callable, Dict, HasTraits, Str, Type, Union


class ServiceOffer(HasTraits):
    """An offer to provide a service."""

    #### 'ServiceOffer' interface #############################################

    #: The protocol that the service provides.
    #:
    #: This can be an actual class or interface, or a string that can be used
    #: to import a class or interface.
    #:
    #: e.g. 'foo.bar.baz.Baz' is turned into 'from foo.bar.baz import Baz'
    protocol = Union(Str, Type)

    #: A callable (or a string that can be used to import a callable) that is
    #: the factory that creates the actual service object.
    #:
    #: e.g::
    #:
    #:   callable(**properties) -> Any
    #:
    #: e.g. 'foo.bar.baz.Baz' is turned into 'from foo.bar.baz import Baz'
    factory = Union(Str, Callable)

    #: An optional set of properties to associate with the service offer.
    #:
    #: This dictionary is passed as keyword arguments to the factory.
    properties = Dict
