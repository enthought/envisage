The "Message of the Day" (MOTD) Example
=======================================

Only marginally more complicated than the traditional "Hello World" example,
this is a simple application that prints a witty, educational, or
inspiring "Message of the Day". Obviously, if we actually had to write this
application, we might not choose to use a framework like Envisage (it is one of
the rare applications that is so simple that why would you bother), but it does
serve to illustrate all of the fundamental aspects of building an Envisage
application.

All of the code for this example can be found in the `examples/MOTD`_ directory
of the Envisage distribution, and to run it simply type::

   cd .../examples/MOTD
   python run.py
  
(or equivalent, depending on your operating system and shell)

Before we dive right in to building our extensible application, let's take a
small, but important, step back. Envisage is designed to be an integration
platform -- a place where you can bring existing code and with a (hopefully)
minimal amount of effort, make it work with the rest of the application.
Because of this, we will start the MOTD example by designing the application
without any knowledge of Envisage whatsoever. This is obviously a good idea in
general, as it allows our code to be reused outside of Envisage applications.

Plain Ol' MOTD
--------------

So lets take a look at our non-Envisage aware MOTD application, the code for
which is in the acme.motd_ package. A good place to start as a developer
*using* any package in Envisage (and, for that matter, the entire Enthought
tool-suite) is to look at any interfaces and classes exposed via its 'api.py'
module.

In this case, there are 2 interfaces

1) IMOTD_

  The interface for simple "Message of the Day" functionality.

2) IMessage_

  The interface supported by each message returned by the motd() method on
  the IMOTD_ interface.

We also (*not* coincidentally!) have 2 corresponding implementation classes:

1) MOTD_
2) Message_

As you can see, the MOTD_ class simply contains a list of messages and
when its motd() method is called, it returns a random choice from that list.

An example of using our MOTD_ class at the Python prompt might be::

    >>> from acme.motd.api import Message, MOTD
    >>> motd = MOTD(messages=[Message(author='Anon', text='Hello World!')])
    >>> message = motd.motd()
    >>> print '"%s" - %s' % (message.text, message.author)
    "Hello World!" - Anon
    >>> 

Well, we had to get "Hello World" in there somewhere!

The important point here is that this code is written without any knowledge of
Envisage or extensibility whatsoever. It is just a small, reusable piece of
code (albeit a very simple one).

Not So Plain Ol' MOTD
---------------------

Now lets look at the steps that we have to go through to use this code and
turn it into an extensible, pluggable Envisage application.

Create the main Application class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First of all, we need to create an object that represents the application
itself. In Envisage, this can be any object that implements the IApplication_
interface, but is usually either an instance of the default Application_ class,
or one derived from it.

In the MOTD_ example, we create the class in the run.py_ module as follows::

    application = Application(
        id      = 'acme.motd',
        plugins = [CorePlugin(), MOTDPlugin(), SoftwareQuotesPlugin()]
    )

    application.run()    

In this case, we use the simplest way to tell Envisage which plugins make up
the application by passing them in explicitly. Envisage applications allow you
to completely configure how plugins are located by setting the plugin manager.
Envisage ships with two plugin managers by default, one that simply takes a
list of plugins as in the above example, and one that finds all plugins
offered via the 'envisage.plugins' entry point in Python Eggs.

The 'acme.motd' plugin
~~~~~~~~~~~~~~~~~~~~~~

As shown above, the corresponding plugin implementation is in the
MOTDPlugin_ class::

  class MOTDPlugin(Plugin):
      """ The 'Message of the Day' plugin.

      This plugin simply prints the 'Message of the Day' to stdout.
    
      """

      # The IDs of the extension points that this plugin offers.
      MESSAGES = 'acme.motd.messages'

      # The IDs of the extension points that this plugin contributes to.
      SERVICE_OFFERS = 'envisage.service_offers'

      #### 'IPlugin' interface ##################################################

      # The plugin's unique identifier.
      id = 'acme.motd'

      # The plugin's name (suitable for displaying to the user).
      name = 'MOTD'

      #### Extension points offered by this plugin ##############################

      # The messages extension point.
      #
      # Notice that we use the string name of the 'IMessage' interface rather
      # than actually importing it. This makes sure that the import only happens
      # when somebody actually gets the contributions to the extension point.
      messages = ExtensionPoint(
          List(Instance('acme.motd.api.IMessage')), id=MESSAGES, desc="""

          This extension point allows you to contribute messages to the 'Message
          Of The Day'.

          """
      )

      #### Contributions to extension points made by this plugin ################

      service_offers = List(contributes_to=SERVICE_OFFERS)

      def _service_offers_default(self):
          """ Trait initializer. """

          # Register the protocol as a string containing the actual module path
          # (do not use a module path that goes via an 'api.py' file as this does
          # not match what Python thinks the module is!). This allows the service
          # to be looked up by passing either the exact same string, or the
          # actual protocol object itself.
          motd_service_offer = ServiceOffer(
              protocol = 'acme.motd.i_motd.IMOTD',
              factory  = self._create_motd_service
          )

          return [motd_service_offer]

      ###########################################################################
      # Private interface.
      ###########################################################################

      def _create_motd_service(self):
          """ Factory method for the 'MOTD' service. """

          # Only do imports when you need to! This makes sure that the import
          # only happens when somebody needs an 'IMOTD' service.
          from motd import MOTD

          return MOTD(messages=self.messages)

      # This plugin does all of its work in this method which gets called when
      # the application has started all of its plugins.
      @on_trait_change('application:started')
      def _print_motd(self):
          """ Print the 'Message of the Day' to stdout! """

          # Note that we always offer the service via its name, but look it up
          # via the actual protocol.
          from acme.motd.api import IMOTD
        
          # Lookup the MOTD service.
          motd = self.application.get_service(IMOTD)

          # Get the message of the day...
          message = motd.motd()

          # ... and print it.
          print '\n"%s"\n\n- %s' % (message.text, message.author)

          return

Although it is obviously a bit of overkill, the example shows how we would
take a MOTD_ object and register it a service for other parts of the
application to use. Sadly, in this example, there are no other parts of the
application, so we just lookup and use the service ourselves!

The 'acme.motd.software_quotes' plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First of all, we have to create the messages that we want to add. Remember that
when the acme.motd_ plugin advertised the extension point, it told us that
every contribution had to implement the IMessage_ interface. Happily, there is
a class that does just that already defined for us (Message_) and so we create
a simple module ('messages.py'_) and add our Message_ instances to it::

    messages = [
        ...
    
        Message(
            author = "Martin Fowler",
            text   = "Any fool can write code that a computer can understand. Good"
            " programmers write code that humans can understand."
        )

        Message(
            author = "Chet Hendrickson",
            text   = "The rule is, 'Do the simplest thing that could possibly"
            " work', not the most stupid."
        )

        ...
    ]

Now we create a plugin for the acme.motd.software_quotes_ package and tell
Envisage about the messages that we have just created::

  class SoftwareQuotesPlugin(Plugin):
      """ The 'Software Quotes' plugin. """

      #### 'IPlugin' interface ##################################################

      # The plugin's unique identifier.
      id = 'acme.motd.software_quotes'

      # The plugin's name (suitable for displaying to the user).
      name = 'Software Quotes'

      #### Contributions to extension points made by this plugin ################

      # Messages for the 'Message Of The Day'.
      messages = List(contributes_to='acme.motd.messages')
    
      ###########################################################################
      # 'SoftwareQuotesPlugin' interface.
      ###########################################################################

      def _messages_default(self):
          """ Trait initializer. """

          # Only do imports when you need to!
          from messages import messages

          return messages

.. _`Python Eggs`: http://peak.telecommunity.com/DevCenter/PythonEggs

.. _acme.motd: https://github.com/enthought/envisage/tree/master/examples/MOTD/acme/motd/api.py

.. _acme.motd.software_quotes: https://github.com/enthought/envisage/tree/master/examples/MOTD/acme/motd/software_quotes/setup.py

.. _Application: https://github.com/enthought/envisage/tree/master/envisage/application.py

.. _`examples/MOTD`: https://github.com/enthought/envisage/tree/master/examples/MOTD

.. _IApplication: https://github.com/enthought/envisage/tree/master/envisage/i_application.py

.. _IMessage: https://github.com/enthought/envisage/tree/master/examples/MOTD/acme/motd/i_message.py

.. _Message: https://github.com/enthought/envisage/tree/master/examples/MOTD/acme/motd/message.py

.. _MOTD: https://github.com/enthought/envisage/tree/master/examples/MOTD/acme/motd/motd.py

.. _IMOTD: https://github.com/enthought/envisage/tree/master/examples/MOTD/acme/motd/i_motd.py

.. _MOTDPlugin: https://github.com/enthought/envisage/tree/master/examples/MOTD/acme/motd/motd_plugin.py

.. _run.py: https://github.com/enthought/envisage/tree/master/examples/MOTD/run.py

