How To Create a Plugin for an Envisage Application
==================================================

This document describes the process of creating an Envisage plugin that works
with a Workbench-based application.

There are several questions to consider when designing a plugin:

* What does it do?
* What functionality does it offer to other plugins?
* What does it add to what other plugins already do?
* What does it need from other plugins?

What Does Your Plugin Do?
-------------------------

"What your plugin does" refers to the basic functionality that your plugin
adds to the application. 

Very often, you want to take some pre-existing chunk of functionality (module,
library, etc.) and make it available within the Envisage application. Assuming
the library has a well-defined API, you do not need to alter it in any way. You 
only create the plugin code to wrap it for Envisage.

Sometimes, however, you are designing a new chunk of functionality just for
the Envisage application. In this case, step back and think about how you
would design the core functionality of the plugin, independent of Envisage. It 
is important to keep this separate from the plugin machinery that make that
functionality work within Envisage.

In either case, we will refer to the code that does this core functionality as
"the library".

Example Library
~~~~~~~~~~~~~~~

Suppose you have a library that implements a game of Tetris. You want to add
this game to an Envisage application that lets users pick a game to play from
a catalog of available games. You have a Tetris class that looks something
like this::
    
    class Tetris(HasTraits):
        
        # Basic colors
        background_color = Color
        foreground_color = Color
        
        # Shapes to use in the game
        shapes = List(IShape)
        ...

In the following sections, we'll look at ways that this library can be
integrated into the application by a plugin.


What Does Your Plugin Offer to Other Plugins?
---------------------------------------------

There are two ways that a plugin can provide functionality to other 
plugins. 

* **Offering services:** Your plugin may provide an API, the core functionality
  of your library, as a service. Yours might be the only provider of that type
  of service in an application, or it might be one of many. 
* **Defining extension points:** Your plugin may offer one or more extension 
  points, which means that your plugin will do something specific with 
  contributions to that extension point. Contributions to an extension point
  must be instances of a type or interface that you specify. An extension point
  is a trait attribute whose type is ExtensionPoint, which consists of a List
  of some other type, plus an ID. In other words, an extension point is a list,
  used by your plugin, that is populated by plugins.
  
Examples of Offering Functionality to Other Plugins
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Suppose that the games application defines an "IGame" interface that it uses to
control games, with methods for starting, stopping, displaying scores, and so
on. In this case, you offer the Tetris library as a service that implements the
"IGame" interface used by the application. (You might need to create an adapter
for your Tetris class to the IGame interface, but we'll ignore that.)

You can manually register a service, but a simple way to do it is to contribute
to the 'envisage.services_offers' extension point of the Core plugin.
This ensures that the plugin is registered, and is created when it is needed.

You also want to allow users to contribute their own Tetris shapes, so you
define an extension point for shapes. We'll leave aside the question of how
users actually define their shapes. The point is that the catalog of shapes is
extensible. (You would probably also contribute some basic shapes from your 
plugin, so that users don't *need* to contribute any.)
  

What Does Your Plugin Add to Other Plugins?
-------------------------------------------

Other plugins may provide extension points that are useful to your plugin. If
so, you can contribute to those extension points. Essentially, your plugin
passes one or more objects to the plugin whose extension point you are 
contributing to, and that plugin "does the right thing" with those items.
  
Examples of Contributing to Extension Points
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Continuing the example of the Tetris game, the application might keep a list
of available games, and present the list for the user to select from. Thus, it
might have a 'games' extension point, to which you can contribute an object
containing information about your Tetris game, such as name, description, icon,
and entry point.

More concretely, you want to specify default colors for the foreground and
background colors of the game, but allow users to change them and save their
changes across sessions. For specifying default preference values and saving
changed values, you can contribute to the 'envisage.preferences'
extension point offered by the Envisage core plugin; for a UI to change
preferences, you can contribute to the
'envisage.ui.workbench.preferences_pages' extension point offered by
the Workbench plugin. (A game application probably wouldn't use the Workbench
plugin, but we'll assume it does to avoid using a fictional plugin.)

A contribution to the preferences extension point must be a URL of a preferences
file (readable by ConfigObj). A plugin typically has only one preferences file,
even if it has many categories of preferences.

A contribution to the preference_pages extension point must be a callable that
returns an object that implements the
`apptools.preferences.ui.api.IPreferencesPage` interface. Such an object
typically has a Traits UI view that can be used in the Preferences dialog box to
set the values of the preference attributes. A plugin may have multiple
preferences pages, depending on how it groups the items to be configured.

There are two strategies for defining a callable that returns an object:

* Subclass from a class that implements the interface, in this case
  `apptools.preferences.ui.api.PreferencesPage`.
* Define a factory function that returns an appropriate object. This strategy
  is not needed for preferences pages, but can be helpful when the object
  being returned contains a reference to a service.

In either case, the contribution is a trait attribute on the plugin object.


What Does Your Plugin Need from Other Plugins?
----------------------------------------------

Your plugin may need to use the API of some other plugin. In Envisage, you use
the other plugin's API via a service, rather than directly. This allows for the
plugin offering the service to be replaced with another one, transparently to
your plugin. There may be multiple plugins offering a particular type of
service, but a client plugin uses only one instance of a service at any given
time. 

Example of Using a Service
~~~~~~~~~~~~~~~~~~~~~~~~~~

The service you use may be your own. For the Tetris game, the object that you
contribute to the application's 'games' extension point needs to be able to
start the game. However, to reduce memory overhead, you don't want the Tetris
library to be imported until the user actually chooses to play Tetris. Using the
service offered by the Tetris plugin is a way to accomplish that.

Complete Example
----------------

The complete plugin for the Tetris game might look like this::
    
    class TetrisPlugin(Plugin):
        """ Plugin to make the Tetris library available in Envisage.
        """
        
        ##### IPlugin Interface ################################################
        
        ### Extension points offered by the plugin
        
        # Shapes to be used in the game
        shape = ExtensionPoint(List(IShape), id='acme.tetris.shapes')
        
        ### Contributions to extension points
        
        my_shapes = List(contributes_to='acme.tetris.shapes')
        def _my_shapes_default(self):
            """ Trait initializer for 'my_shapes' contribution to this plugin's
                own 'shapes' extension point.
            """
            return [ Shape1(), Shape2(), Shape3() ]

        games = List(contributes_to='acme.game_player.game_infos'
        def _games_default(self):
            """ Trait initializer for 'games' contribution to the application
                plugin's 'games' extension point.
            """
            return [ GameInfo(name='Tetris', icon='tetris.png',
                              description='Classic shape-fitting puzzle game',
                              entry_point=self._start_game) ]
        
        preferences = List(contributes_to='envisage.preferences')
        def _preferences_default(self):
            """ Trait initializer for 'preferences' contribution. """
            return ['pkgfile://acme.tetris.plugin/preferences.ini']
            
        preferences_pages = List(contributes_to=
            'envisage.ui.workbench.preferences_pages')
        def _preferences_pages_default(self):
            """ Trait initializer for 'preferences_pages' contribution. """
            from acme.tetris.plugin.preferences_pages import \
                TetrisPreferencesPages
            return [ TetrisPreferencesPages ]
            
        services_offers = List(contributes_to='envisages.service_offers')
        def _service_offers_default(self):
            """ Trait initializer for 'service_offers' contribution. """
            return [ ServiceOffer(protocol=IGame, 
                                  factory=self._create_tetris_service,
                                  properties={'name':'tetris'}) ]
                                  
        #### Private interface #################################################
        
        def _create_tetris_service(self, **properties):
            """ Factory method for the Tetris service. """
            tetris = Tetris() # This creates the non-Envisage library object.
            
            # Hook up the extension point contributions to the library object trait.
            bind_extension_point(tetris, 'shapes', 'acme.tetris.shapes')
            
            # Hook up the preferences to the library object traits.
            bind_preference(tetris, 'background_color', 
                            'acme.tetris.background_color')
            bind_preference(tetris, 'foreground_color',
                            'acme.tetris.foreground_color')
            return tetris
            
        def _start_game(self):
            """ Starts a Tetris game. """
            game = self.application.get_service(IGame, "name == 'tetris'")
            game.start()
            
