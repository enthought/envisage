# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" A plugin manager that gets its plugins from Eggs. """


# Standard library imports.
import logging
import re
import warnings

# 3rd party imports.
import pkg_resources

# Enthought library imports.
from traits.api import Instance, List, Str

# Local imports.
from .egg_utils import get_entry_points_in_egg_order
from .plugin_manager import PluginManager

# Logging.
logger = logging.getLogger(__name__)


class EggPluginManager(PluginManager):
    """A plugin manager that gets its plugins from Eggs.

    To declare a plugin (or plugins) in your egg use an entry point in your
    'setup.py' file, e.g.

    [envisage.plugins]
    acme.foo = acme.foo.foo_plugin:FooPlugin

    The left hand side of the entry point declaration must be the same as the
    'id' trait of the plugin (e.g. the 'FooPlugin' would have its 'id' trait
    set to 'acme.foo'). This allows the plugin manager to filter out plugins
    using the 'include' and 'exclude' lists (if specified) *without* having to
    import and instantiate them.

    """

    def __init__(self, **traits):
        warnings.warn(
            (
                "The EggPluginManager is deprecated. The recommended "
                "approach is to install plugin-containing packages into "
                "site-packages and advertise the plugins via entry points. "
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(**traits)

    # Entry point Id.
    PLUGINS = "envisage.plugins"

    #### 'EggPluginManager' interface #########################################

    # The working set that contains the eggs that contain the plugins that
    # live in the house that Jack built ;^) By default we use the global
    # working set.
    working_set = Instance(pkg_resources.WorkingSet)

    # An optional list of the Ids of the plugins that are to be excluded by
    # the manager.
    #
    # Each item in the list is actually a regular expression as used by the
    # 're' module.
    exclude = List(Str)

    # An optional list of the Ids of the plugins that are to be included by
    # the manager (i.e. *only* plugins with Ids in this list will be added to
    # the manager).
    #
    # Each item in the list is actually a regular expression as used by the
    # 're' module.
    include = List(Str)

    ###########################################################################
    # Protected 'PluginManager' interface.
    ###########################################################################

    def __plugins_default(self):
        """Trait initializer."""

        plugins = []
        for ep in get_entry_points_in_egg_order(
            self.working_set, self.PLUGINS
        ):
            if self._is_included(ep.name) and not self._is_excluded(ep.name):
                plugin = self._create_plugin_from_ep(ep)
                plugins.append(plugin)

        logger.debug("egg plugin manager found plugins <%s>", plugins)

        return plugins

    def _working_set_default(self):
        """Trait initializer."""

        return pkg_resources.working_set

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_plugin_from_ep(self, ep):
        """Create a plugin from an extension point."""

        klass = ep.load()
        plugin = klass(application=self.application)

        # Warn if the entry point is an old-style one where the LHS didn't have
        # to be the same as the plugin Id.
        if ep.name != plugin.id:
            logger.warning(
                "entry point name <%s> should be the same as the "
                "plugin id <%s>" % (ep.name, plugin.id)
            )

        return plugin

    def _is_excluded(self, plugin_id):
        """Return True if the plugin Id is excluded.

        If no 'exclude' patterns are specified then this method returns False
        for all plugin Ids.

        """

        if len(self.exclude) == 0:
            return False

        for pattern in self.exclude:
            if re.match(pattern, plugin_id) is not None:
                return True

        return False

    def _is_included(self, plugin_id):
        """Return True if the plugin Id is included.

        If no 'include' patterns are specified then this method returns True
        for all plugin Ids.

        """

        if len(self.include) == 0:
            return True

        for pattern in self.include:
            if re.match(pattern, plugin_id) is not None:
                return True

        return False
