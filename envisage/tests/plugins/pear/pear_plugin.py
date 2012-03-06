""" The 'Pear' plugin """


from envisage.api import Plugin
from traits.api import Bool


class PearPlugin(Plugin):
    """ The 'Pear' plugin """

    #### 'IPlugin' protocol ####################################################

    # The plugin's unique identifier.
    id = 'pear'

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

    #### 'BananaPlugin' protocol ###############################################

    started = Bool(False)
    stopped = Bool(False)

#### EOF ######################################################################
