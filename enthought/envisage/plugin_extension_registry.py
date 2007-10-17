""" An extension registry that uses plugins as extension providers. """


# Enthought library imports.
from enthought.traits.api import Instance, List, Undefined, on_trait_change

# Local imports.
from i_application import IApplication
from i_extension_provider import IExtensionProvider
from provider_extension_registry import ProviderExtensionRegistry


# fixme: Can we add something like these to traits? I hate the remove=True
# API!?!
def connect(obj, handler, trait_name=None, dispatch='same'):
    """ Connect a dynamic trait change handler. """

    obj.on_trait_change(handler, trait_name, dispatch=dispatch)
    
    return
    
def disconnect(obj, handler, trait_name=None, dispatch='same'):
    """ Connect a dynamic trait change handler. """
    
    obj.on_trait_change(handler, trait_name, dispatch=dispatch, remove=True)
    
    return


class PluginExtensionRegistry(ProviderExtensionRegistry):
    """ An extension registry that uses plugins as extension providers. """

    #### 'IProviderExtensionRegistry' interface ###############################

    # The extension providers that populate the registry.
    #
    # There is currently no way to express this in traits, but this trait is
    # readonly, meaning that you can use the list to iterate over all of the
    # items in it, and you can listen for changes to the list, but if you want
    # to add or remove a provider you should call 'add_provider' or
    # 'remove_provider' respectively.
    providers = List(IExtensionProvider)

    # fixme: We would like to use::
    #
    # providers = Delegate('application', 'plugins')
    #
    # but there are oustanding bugs with traits that prevent this from working
    # as expected.
    
    #### 'PluginExtensionRegistry' interface ##################################

    # The application that the registry is part of.
    application = Instance(IApplication)

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Constructor. """

        super(PluginExtensionRegistry, self).__init__(**traits)

    #### Trait change handlers ################################################

    ###########################################################################
    # Private interface.
    ###########################################################################

##     def _application_changed(self, trait_name, old, new):
##         """ Static trait change handler. """

##         if new is not None:
##             new.sync_trait('plugins', self, 'providers')

##         return

##     def _providers_changed(self, trait_name, old, new):
##         """ Static trait change handler. """

##         print 'PER._providers_changed', old, new
        
##         self._update_providers(old, new)

##         return

##     def _providers_items_changed(self, trait_name, old, event):
##         """ Static trait change handler. """

##         print 'PER._providers_changed', event.removed, event.added
        
##         self._update_providers(event.removed, event.added)

##         return

    #### Trait change handlers ################################################

    def _application_changed(self, trait_name, old, new):
        """ Static trait change handler. """

        if old is not None:
            disconnect(old, self._on_plugins_changed, 'plugins')
            disconnect(old, self._on_plugins_items_changed, 'plugins_items')

            self._update_providers(old.plugins, [])
            
        if new is not None:
            connect(new, self._on_plugins_changed, 'plugins')
            connect(new, self._on_plugins_items_changed, 'plugins_items')

            self._update_providers([], new.plugins)

        return

    def _on_plugins_changed(self, obj, trait_name, old, new):
        """ Dynamic trait change handler. """

        self._update_providers(old, new)
        
        return

    def _on_plugins_items_changed(self, obj, trait_name, old, event):
        """ Dynamic trait change handler. """

        self._update_providers(event.removed, event.added)

        return
    
    #### Methods ##############################################################

    def _update_providers(self, removed, added):
        """ Add/remove the specified providers. """

        for plugin in removed:
            self.remove_provider(plugin)

        for plugin in added:
            self.add_provider(plugin)

        return

#### EOF ######################################################################
