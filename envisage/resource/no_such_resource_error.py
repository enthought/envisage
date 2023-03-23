# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The exception raised when trying to open a non-existent resource. """


class NoSuchResourceError(Exception):
    """The exception raised when trying to open a non-existent resource."""

    def __init__(self, message=""):
        """Constructor."""

        Exception.__init__(self, message)
