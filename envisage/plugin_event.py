# (C) Copyright 2007-2025 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" A plugin event. """


# Enthought library imports.
from traits.api import Instance, Vetoable


class PluginEvent(Vetoable):
    """A plugin event."""

    # The plugin that the event is for.
    plugin = Instance("envisage.api.IPlugin")
