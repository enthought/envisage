# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" The plugin activator interface. """


# Enthought library imports.
from traits.api import Interface


class IPluginActivator(Interface):
    """ The plugin activator interface.

    A plugin activator is really just a collection of two strategies - one
    to start the plugin and one to stop it.

    We use an activator so that the framework can implement default start and
    stop strategies without forcing the plugin writer to call 'super' if they
    override the 'start' and 'stop' methods on 'IPlugin'.

    I'm not sure that having to call 'super' is such a burden, but some people
    seem to like it this way, and it does mean one less thing for a plugin
    writer to have to remember to do!

    """

    def start_plugin(self, plugin):
        """ Start the specified plugin.

        """

    def stop_plugin(self, plugin):
        """ Stop the specified plugin.

        """

#### EOF ######################################################################
