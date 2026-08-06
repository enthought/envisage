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
take a look at the |Message of the Day| example included in the Envisage
distribution. This example shows how to build a very simple application that
prints a (hopefully witty, educational, or inspiring) "Message of the Day"
chosen at random from a list of contributed messages.

Declaring an Extension Point
----------------------------

Plugins declare the extension points declaratively - using the |ExtensionPoint|
trait type. Note that extension points can also be defined programmatically -
by overriding the 'get_extension_points' method.

In the MOTD example, the |acme.motd| plugin needs to advertise an extension
point that allows other plugins to contribute new messages. Using the
|ExtensionPoint| trait type, the plugin would look like this::

    class MOTDPlugin(Plugin):
        """ The MOTD Plugin. """"

	...

	#: The messages extension point.
	messages = ExtensionPoint(
            List(IMessage), id='acme.motd.messages', desc = """

            This extension point allows you to contribute messages to the 'Message
            Of The Day'.

            """
        )

	...

This tells us three things about the extension point:

1) That the extension point is called "acme.motd.messages"
2) That every item in a list of contributions to the extension point must
   implement the |IMessage| interface.
3) That the extension point allows you to contribute messages!

Making contributions to an Extension Point
------------------------------------------

The |Message of the Day| example has a second plugin,
|acme.motd.software_quotes| that contributes some pithy quotes about software
development to the application.

First of all, we have to create the messages that we want to add. Remember that
when the |acme.motd| plugin advertised the extension point, it told us that
every contribution had to implement the |IMessage| interface. Happily, there is
a class that does just that already defined for us (|Message|) and so we create
a simple module (|messages.py|) and add our |Message| instances to it::

    messages = [
        ...
        Message(
            author="Martin Fowler",
            text=(
                "Any fool can write code that a computer can understand. Good"
                " programmers write code that humans can understand."
            ),
        ),
        Message(
            author="Chet Hendrickson",
            text=(
                "The rule is, 'Do the simplest thing that could possibly"
                " work', not the most stupid."
            ),
        ),
        ...
    ]

Now we create a plugin for the |acme.motd.software_quotes| package and tell
Envisage about the messages that we have just created. This can be done
declaratively - using the 'contributes_to' trait metadata. Note that this can
also be achieved programmatically - by overriding the 'get_extensions' method,
similar to how we could define extension points programmatically by overriding
the 'get_extension_points' method.

The declarative version looks like this::

    class SoftwareQuotesPlugin(Plugin):
        """ The software quotes plugin. """

        ...

        # The 'contributes_to' trait metadata tells Envisage the ID of the
        # extension point that this trait contributes to.
        messages = List(contributes_to='acme.motd.messages')

        def _messages_default(self):
            """ Returns the default value for the ``messages`` trait. """

            # It is good practise to only import your extensions when they
            # are actually required.
            from .messages import messages

            return messages

        ...

The messages are contributed simply by creating a list trait and setting its
"contributes_to" metadata to the ID of the extension point that we want to
contribute to. All we have to do then is to intialize the trait with our
messages and "Job done"!

Note that if a plugin changes a list of contributions then the extension
registry will be updated automatically, and anybody that is consuming the
extensions will be notified accordingly.

The difference between the programmatic and the declarative version is that the
application is not automatically notified if the plugin wants to change its
contributions to an extension point. To do this manually fire an
'extension_point_changed' event.

Retrieving the contributions to an Extension Point
--------------------------------------------------

OK, here's where we are so far: One plugin (|acme.motd|) has advertised the fact
that it has an extension point called "acme.motd.messages", and that the
contributions to the extension point must implement the |IMessage| interface.
Another plugin (|acme.motd.software_quotes|) has kindly offered to contribute
some messages about software development. Now we need to know how to retrieve
the contributed messages at runtime.

In the MOTD example, the messages are retrieved by the |acme.motd| plugin::

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
            """ Returns the default value for the motd trait. """

            # Only do imports when you need to!
            from .motd import MOTD

            return MOTD(messages=self.messages)
        ...

As you can see, all we have to do is to access the **messages** extension point
trait when we create our instance of the |MOTD| class.

This example demonstrates a common pattern in Envisage application development,
in that contributions to extension points are most often used by plugin
implementations to create and initialize services (in this case, an instance of
the |MOTD| class).

The extension registry can also be accessed through the following method on the
|IApplication| interface::

    def get_extensions(self, extension_point):
        """ Return a list containing all contributions to an extension point.

        Return an empty list if the extension point does not exist.

        """

For example, to get the messages contributed to the "acme.motd.messages"
extension point you would use::

    messages = application.get_extensions('acme.motd.messages')

Note however, that using the |ExtensionPoint| trait type, adds the ability to
validate the contributions -- in this case, to make sure that they are all
objects that implement (or can be adapted to) the |IMessage| interface. It also
automatically connects the trait so that the plugin will receive trait change
events if extensions are added/removed to/from the extension point at runtime.
