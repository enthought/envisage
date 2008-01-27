""" The 'Message of the Day' plugin """


# In the interest of lazy loading you should only import from the following
# packages at the module level of a plugin::
#
# - enthought.envisage
# - enthought.traits
#
# Eveything else should be imported when it is actually required.


# Enthought library imports.
from enthought.envisage.api import ExtensionPoint, Plugin
from enthought.traits.api import Instance, List


class MOTDPlugin(Plugin):
    """ The 'Message of the Day' plugin.

    When this plugin is started it prints the 'Message of the Day' to stdout.
    
    """

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'acme.motd'

    # The plugin's name (suitable for displaying to the user).
    name = 'MOTD'

    #### 'MOTDPlugin' interface ###############################################
    
    ###########################################################################
    # Extension points offered by this plugin.
    ###########################################################################

    # The messages extension point.
    #
    # Notice that we use the string name of the 'IMessage' interface rather
    # than actually importing it. This makes sure that the import only happens
    # when somebody actually gets the contributions to the extension point.
    messages = ExtensionPoint(
        List(Instance('acme.motd.api.IMessage')),
        id   = 'acme.motd.messages',
        desc = """

        This extension point allows you to contribute messages to the 'Message
        Of The Day'.

        """
    )

    ###########################################################################
    # Contributions to extension points made by this plugin.
    ###########################################################################

    # None

    ###########################################################################
    # Services offered by this plugin.
    ###########################################################################

    # The 'MOTD' service.
    #
    # Notice that we use the string name of the 'IMOTD' interface rather than
    # actually importing it. This makes sure that the import only happens when
    # somebody needs an 'IMOTD' service.
    motd = Instance('acme.motd.api.IMOTD', service=True)
    
    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    def start(self):
        """ Start the plugin. """

        # This is a bit of overkill here, but it shows how other plugins can
        # look up the MOTD service. We could, of course, just use::
        #
        #    message = self.motd.motd()
        #
        # Get the message of the day...
        message = self.application.get_service('acme.motd.api.IMOTD').motd()

        # ... and print it.
        print '\n"%s"\n\n- %s' % (message.text, message.author)
        
        return

    ###########################################################################
    # 'MOTDPlugin' interface.
    ###########################################################################

    def _motd_default(self):
        """ Trait initializer. """

        # Only do imports when you need to! This makes sure that the import
        # only happens when somebody needs an 'IMOTD' service.
        from motd import MOTD

        return MOTD(messages=self.messages)
    
#### EOF ######################################################################
