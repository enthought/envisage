""" The 'Foo' plugin """


# Enthought library imports.
from envisage.api import Plugin
from traits.api import Bool


class AcmePlugin(Plugin):
    """ The 'Acme' plugin """

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'acme.acme'

    #### 'AcmePlugin' interface ################################################

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
