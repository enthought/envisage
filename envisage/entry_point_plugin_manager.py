# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


from traits.api import Instance, List, Str, Union

from envisage.plugin_manager import PluginManager


try:
    from importlib.metadata import EntryPoints, entry_points
except ImportError:
    from importlib_metadata import EntryPoints, entry_points


class EntryPointPluginManager(PluginManager):

    group = Str("envisage.plugins")

    #: Entry points that the plugins will be loaded from.
    # XXX Add some kind of name-based filtering on top of this.
    entry_points = Instance(EntryPoints)

    def _entry_points_default(self):
        # XXX Find a way to test this. Likely needs an integration test.
        # Though we can safely test with envisage.plugins.
        return entry_points(group=self.group)

    # Protected 'PluginManager' protocol ######################################

    def __plugins_default(self):
        return [
            entry_point.load()()
            for entry_point in self.entry_points
        ]
