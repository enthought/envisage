Plugins
=======

*Plugins* are used to "deliver" `Extension Points`_, contributions to extension
points, and Services_ into an Envisage application. In fact, plugins can be
thought of as simply being "delivery trucks" -- they rarely (if ever) do any
*real* work themselves. In other words, plugins can do 3 things:

1) Declare extension points
2) Make contributions to extension points (including its own)
3) Create and publish services

Plugins are located and managed by the *plugin manager*, and, whilst Envisage
is designed such that you can write your own plugin manager, by default, it
uses an implementation based on `Python Eggs`_.

Creating a Plugin
-----------------

All plugins must implement the IPlugin_ interface (an easy way to achieve this
is to subclass the base Plugin_ class), and should provide the following
"housekeeping" information:

- a globally unique identifier (e.g., "acme.motd")

  This obviously allows Envisage to identify a particular plugin in a sea of
  other plugins. Technically, this identifier only need be unique within your
  application, but since the intent is for applications to be able to include
  plugins from (potentially) all over the world, using the common reverse
  domain name notation is probably a good idea!

- a name

  This name should be suitable for display to the user.

- a doc string!

  A nice description of the intent and features of your plugin.

Here is a snippet from the `acme.motd`_ plugin that is part of the `Message of
the Day`_ example::

    class MOTDPlugin(Plugin):
        """ The 'Message of the Day' plugin.

	When this plugin is started it prints the 'Message of the Day' to stdout.

        """

        #### 'IPlugin' interface ##############################################

        # The plugin's unique identifier.
        id = 'acme.motd'

        # The plugin's name (suitable for displaying to the user).
        name = 'MOTD'

Plugin Lifecycle
----------------

Plugins have a lifecycle in the context of an application. There are currently
two key lifecycle methods on the IPlugin_ interface::

    def start(self):
        """ Start the plugin.

        This method is called by the framework when the application is starting
        up. If you want to start a plugin manually use::

          application.start_plugin(plugin)

        """

    def stop(self):
        """ Stop the plugin.

        This method is called by the framework when the application is
        stopping. If you want to stop a plugin manually use::

          application.stop_plugin(plugin)

        """

When Envisage starts up it calls the start() method of every plugin in the
the same order that its iterator returns them in. This depends on the plugin
manager being used, but by default this will be either a) the order of the list
of plugins that was passed into the application or b) the order of the plugins
based on egg dependencies. When the application stops, it calls the stop()
method of each plugin in the reverse order that they were started in.


.. _`Extension Points`: extension_points.html
.. _`Python Eggs`: http://peak.telecommunity.com/DevCenter/PythonEggs
.. _Services: services.html

.. _acme.motd: https://github.com/enthought/envisage/tree/master/examples/MOTD/acme/motd/setup.py

.. _IPlugin: https://github.com/enthought/envisage/tree/master/envisage/i_plugin.py

.. _`Message of the Day`: https://github.com/enthought/envisage/tree/master/examples/MOTD

.. _MOTD: https://github.com/enthought/envisage/tree/master/examples/MOTD/acme/motd/motd.py

.. _Plugin: https://github.com/enthought/envisage/tree/master/envisage/plugin.py
