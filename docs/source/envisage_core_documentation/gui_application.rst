GUIApplication
==============

The :py:class:`GUIApplication` subclass of the standard Envisage
:py:class:`Application` class uses PyFace's cross-platform GUI tools to ensure
that an appropriate back-end application object is instantiated before plugins
run their :py:meth:`start` methods, and then ensures that the GUI mainloop is
started after the :py:meth:`start` methods have successfully completed.

This allows developers to have a single place to start the application, but have
plugins to listen for the :py:attr:`application_initialized` event to create UI
components.  In particular, Traits UIs can be created in an event listener
method by calling :py:meth:`edit_traits`, something like this::

    class MyViewPlugin(Plugin):

        model = Instance

        ui = Instance('traitsui.ui.UI')

        @on_trait_change('application:application_initialized')
        def create_ui(self):
            # we need to keep a reference to the ui object
            self.ui = self.model.edit_traits()

This is intended to be a cheap and simple way to take an existing application
and start "lifting" it to Envisage, without having to use a more heavyweight
UI framework such as Tasks immediately.  Developers can work on adding
extensibility to the application's model without having to at the same time
add extensibility to their UI.

The :py:class:`GUIApplication` exposes the following public API:

.. py:attribute:: gui

    The PyFace :py:class:`GUI` instance the :py:class:`GUIApplication` creates.

.. py:attribute:: splash_screen

    An optional PyFace :py:class:`ISplashScreen` that gets shown while
    the plugins are started.

.. py:attribute:: application_initialized

    An event which is fired after the UI mainloop has started.
