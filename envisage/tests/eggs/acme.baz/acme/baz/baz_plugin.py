""" The 'Baz' plugin """


# Enthought library imports.
from envisage.api import Plugin
from traits.api import Bool


class BazPlugin(Plugin):
    """ The 'Baz' plugin """

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'acme.baz'

    #### 'BazPlugin' interface ################################################

    started = Bool(False)
    stopped = Bool(False)

    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

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

#### EOF ######################################################################
