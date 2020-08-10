# (C) Copyright 2007-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The 'Banana' plugin """


from envisage.api import Plugin
from traits.api import Bool


class BananaPlugin(Plugin):
    """ The 'Banana' plugin """

    #### 'IPlugin' protocol ###################################################

    # The plugin's unique identifier.
    id = "banana"

    def start(self):
        """ Start the plugin. """

        self.started = True
        self.stopped = False

        return

    def stop(self):
        """ Stop the plugin. """

        self.started = False
        self.stopped = True

        return

    #### 'BananaPlugin' protocol ##############################################

    started = Bool(False)
    stopped = Bool(False)
