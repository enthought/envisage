Extension Points
================

Whether or not we as software developers like to admit it, most (if not all) of
the applications we write need to change over time. We fix bugs, and we add, 
modify, and remove features. In other words, we spend most of our time either
fixing or extending applications.

Sometimes we extend our applications by changing the actual code, sometimes
we have other ad hoc extension mechanisms in place -- a text file here,
a directory of scripts there. As applications grow, they often end up with
numerous places where they can be extended, but with a different extension
mechanism at each one. This makes it hard for developers who want to extend
the application to know a) *where* they can add extensions, and b) *how*
to add them.

Envisage attempts to address this problem by admitting up front that 
applications need to be extensible, and by providing a standard way for
developers to advertise the places where extension can occur (known as
*extension points*), and for other developers to contribute *extensions* to
them.

In Envisage, extension points and the extensions contributed to them are stored
in the *extension registry*. To see how extension points actually work, let's
take a look at the `Message of the Day`_ example included in the Envisage
distribution. This example shows how to build a very simple application that
prints a (hopefully witty, educational, or inspiring) "Message of the Day"
chosen at random from a list of contributed messages.

Declaring an Extension Point
----------------------------

Plugins declare their extension points in one of two ways:

1) Declaratively - using the 'ExtensionPoint' trait type
2) Programmatically - by overriding the 'get_extension_points' method.

In the MOTD example, the acme.motd_ plugin needs to advertise an extension
point that allows other plugins to contribute new messages. Using the
'ExtensionPoint' trait type, the plugin would look like this::

    class MOTDPlugin(Plugin):
        """ The MOTD Plugin. """"

	...

	# The messages extension point.
	messages = ExtensionPoint(
            List(IMessage), id='acme.motd.messages', desc = """

            This extension point allows you to contribute messages to the 'Message
            Of The Day'.

            """
        )

	...

Overriding the 'get_extension_points' method might look somthing like::

    class MOTDPlugin(Plugin):
        """ The MOTD Plugin. """"

	...

	def get_extension_points(self):
            """ Return the plugin's extension points. """

     	    messages = ExtensionPoint(
                List(IMessage), id='acme.motd.messages', desc = """

                This extension point allows you to contribute messages to the 'Message
                Of The Day'.

                """
            )

            return [messages]

	...


Either way, this tells us three things about the extension point:

1) That the extension point is called "acme.motd.messages"
2) That every item in a list of contributions to the extension point must
   implement the IMessage_ interface.
3) That the extension point allows you to contribute messages!

Making contributions to an Extension Point
------------------------------------------

The `Message of the Day`_ example has a second plugin,
acme.motd.software_quotes_ that contributes some pithy quotes about software
development to the application.

First of all, we have to create the messages that we want to add. Remember that
when the acme.motd_ plugin advertised the extension point, it told us that
every contribution had to implement the IMessage_ interface. Happily, there is
a class that does just that already defined for us (Message_) and so we create
a simple module (messages.py_) and add our Message_ instances to it::

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
Envisage about the messages that we have just created. Again there are are
two ways that a plugin can do this:

1) Declaratively - using the 'contributes_to' trait metadata
2) Programmatically - by overriding the 'get_extensions' method.

The declarative version looks like this::

    class SoftwareQuotesPlugin(Plugin):
        """ The software quotes plugin. """

        ...

        # The 'contributes_to' trait metadata tells Envisage the ID of the
        # extension point that this trait contributes to.
	messages = List(contributes_to='acme.motd.messages')

        def _messages_default(self):
            """ Trait initializer. """

	    # It is good practise to only import your extensions when they
	    # are actually required.
	    from messages import messages

	    return messages

	...

The messages are contributed simply by creating a list trait and setting its
"contributes_to" metadata to the ID of the extension point that we want to
contribute to. All we have to do then is to intialize the trait with our
messages and "Job done"!

Note that if a plugin changes a list of contributions then the extension
registry will be updated automatically, and anybody that is consuming the
extensions will be notified accordingly.

The programmatic version looks like this::

    class SoftwareQuotesPlugin(Plugin):
        """ The software quotes plugin. """

        ...

	def get_extensions(self, extension_point_id):
            """ Get the plugin's contributions to an extension point. """

	    if extension_point_id == 'acme.motd.messages':
	        from messages import messages

                extensions = messages

	    else:
                extensions = []

            return extensions

	...

The difference between this and the declarative version is that the application
is not automatically notified if the plugin wants to change its contributions
to an extension point. To do this manually fire an 'extension_point_changed'
event.

Retrieving the contributions to an Extension Point
--------------------------------------------------

OK, here's where we are so far: One plugin (acme.motd_) has advertised the fact
that it has an extension point called "acme.motd.messages", and that the
contributions to the extension point must implement the IMessage_ interface.
Another plugin (acme.motd.software_quotes_) has kindly offered to contribute
some messages about software development. Now we need to know how to retrieve
the contributed messages at runtime.

In the MOTD example, the messages are retrieved by the acme.motd_ plugin::

    class MOTDPlugin(Plugin):
        """ The MOTD Plugin. """"

	...

	# The messages extension point.
	messages = ExtensionPoint(
            List(IMessage), id='acme.motd.messages', desc = """

            This extension point allows you to contribute messages to the 'Message
            Of The Day'.

            """
        )

	...

        def _motd_default(self):
            """ Trait initializer. """

            # Only do imports when you need to!
            from motd import MOTD

            return MOTD(messages=self.messages)

            ...

As you can see, all we have to do is to access the **messages** extension point
trait when we create our instance of the MOTD_ class.

This example demonstrates a common pattern in Envisage application development,
in that contributions to extension points are most often used by plugin
implementations to create and initialize services (in this case, an instance of
the MOTD_ class).

The extension registry can also be accessed through the following method on the
IApplication_ interface::

    def get_extensions(self, extension_point):
        """ Return a list containing all contributions to an extension point.

        Return an empty list if the extension point does not exist.

        """

For example, to get the messages contributed to the "acme.motd.messages"
extension point you would use::

    messages = application.get_extensions('acme.motd.messages')

Note however, that using the ExtensionPoint_ trait type, adds the ability to
validate the contributions -- in this case, to make sure that they are all
objects that implement (or can be adapted to) the IMessage_ interface. It also
automatically connects the trait so that the plugin will receive trait change
events if extensions are added/removed to/from the extension point at runtime.


.. _`Python Eggs`: http://peak.telecommunity.com/DevCenter/PythonEggs

.. _acme.motd: https://github.com/enthought/envisage/tree/master/examples/MOTD/acme/motd/motd_plugin.py

.. _acme.motd.software_quotes: https://github.com/enthought/envisage/tree/master/examples/MOTD/acme/motd/software_quotes/software_quotes_plugin.py

.. _ExtensionPoint: https://github.com/enthought/envisage/tree/master/envisage/extension_point.py

.. _IApplication: https://github.com/enthought/envisage/tree/master/envisage/i_application.py

.. _IMessage: https://github.com/enthought/envisage/tree/master/examples/MOTD/acme/motd/i_message.py

.. _Message: https://github.com/enthought/envisage/tree/master/examples/MOTD/acme/motd/message.py

.. _messages.py: https://github.com/enthought/envisage/tree/master/examples/MOTD/acme/motd/software_quotes/messages.py

.. _`Message of the Day`: https://github.com/enthought/envisage/tree/master/examples/MOTD

.. _MOTD: https://github.com/enthought/envisage/tree/master/examples/MOTD/acme/motd/motd.py

.. _MOTDPlugin: https://github.com/enthought/envisage/tree/master/examples/MOTD/acme/motd/motd_plugin.py
