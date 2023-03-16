# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


try:
    from importlib.metadata import entry_points, EntryPoints
except ImportError:
    from importlib_metadata import entry_points, EntryPoints

from traits.api import Instance, Str

from envisage.plugin_manager import PluginManager


class EntryPointPluginManager(PluginManager):
    """
    A plugin manager that loads the initial set of plugins from
    a collection of Python entry points (see importlib.metadata).
    """

    #: Name of the entry point group that we'll load plugins from, if
    #: the 'entry_points' trait is not provided.
    group = Str("envisage.plugins")

    #: Entry points that the plugins will be loaded from. Overrides
    #: the 'group' trait.
    entry_points = Instance(EntryPoints)

    def _entry_points_default(self):
        return entry_points(group=self.group)

    # Protected 'PluginManager' protocol ######################################

    def __plugins_default(self):
        return [entry_point.load()() for entry_point in self.entry_points]
