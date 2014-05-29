""" A view showing a summary of the running application. """


# Standard library imports.
import inspect

# Enthought library imports.
from envisage.api import IApplication, IExtensionPoint
from envisage.api import IExtensionRegistry
from envisage.developer.code_browser.api import CodeBrowser
from apptools.io.api import File
from traits.api import HasTraits, Instance
from traitsui.api import Item, TreeEditor, View

# fixme: non-api import.
from envisage.plugins.text_editor.editor.text_editor import TextEditor

# Local imports.
from .extension_registry_browser_tree import \
     extension_registry_browser_tree_nodes


extension_registry_browser_view = View(
    Item(
        name       = 'extension_registry',
        show_label = False,
        editor     = TreeEditor(
            nodes       = extension_registry_browser_tree_nodes,
            editable    = False,
            orientation = 'vertical',
            hide_root   = True,
            show_icons  = True,
            on_dclick   = 'object.dclick'
        )
    ),

    resizable = True,
    style     = 'custom',
    title     = 'Extension Registry',

    width     = .1,
    height    = .1
)


class ExtensionRegistryBrowser(HasTraits):
    """ An extension registry browser.

    Actually, this class exists just because to use a trait editor we have
    to have a trait to edit!

    """

    #### 'ExtensionRegistryBrowser' interface #################################

    # The application that whose extension registry we are browsing.
    application = Instance(IApplication)

    # The code browser that we use to parse plugin source code.
    code_browser = Instance(CodeBrowser)

    # The extension registry that we are browsing.
    extension_registry = Instance(IExtensionRegistry)

    # The workbench service.
    workbench = Instance('envisage.ui.workbench.api.Workbench')

    # The default traits UI view.
    traits_view = extension_registry_browser_view

    ###########################################################################
    # 'ExtensionRegistryBrowser' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _extension_registry_default(self):
        """ Trait initializer. """

        return self.application

    def _workbench_default(self):
        """ Trait initializer. """

        from envisage.ui.workbench.api import Workbench

        return self.application.get_service(Workbench)

    #### Methods ##############################################################

    def dclick(self, obj):
        """ Called when an object in the tree is double-clicked. """

        # Double-click on an extension point.
        if IExtensionPoint(obj, None) is not None:
            self.dclick_extension_point(obj)

        # Double-click on an extension.
        elif IExtensionPoint(obj.parent.value, None) is not None:
            self.dclick_extension(obj)

        return

    def dclick_extension_point(self, obj):
        """ Called when an extension point is double-clicked. """

        # Find the plugin that offered the extension point.
        plugin = self._get_plugin(obj)

        # Parse the plugin source code.
        module = self._parse_plugin(plugin)

        # Get the plugin klass.
        klass = self._get_plugin_klass(module, plugin)

        # Edit the plugin.
        editor = self.workbench.edit(
            self._get_file_object(plugin), kind=TextEditor
        )

        # Was the extension point offered declaratively via a trait?
        trait_name = self._get_extension_point_trait(plugin, obj.id)
        if trait_name is not None:
            attribute = klass.attributes.get(trait_name)
            lineno    = attribute.lineno

        else:
            lineno = klass.lineno

        editor.select_line(lineno)

        return

    def dclick_extension(self, obj):
        """ Called when an extension is double-clicked. """

        extension_point = obj.parent.value
        index           = obj.parent._index

        extension_registry = self.extension_registry
        extensions = extension_registry.extension_registry._extensions

        total = 0
        provider_index = 0
        for l in extensions[extension_point.id]:
            total = total + len(l)
            if index < total:
                break
            provider_index += 1


        plugin = extension_registry.extension_registry._providers[provider_index]

        # Parse the plugin source code.
        module = self._parse_plugin(plugin)

        # Get the plugin klass.
        klass = self._get_plugin_klass(module, plugin)

        # Edit the plugin.
        editor = self.workbench.edit(
            self._get_file_object(plugin), kind=TextEditor
        )

        # Was the extension offered declaratively?
        trait_name = self._get_extension_trait(plugin, extension_point.id)
        if trait_name is not None:

            # Does the trait have a default initializer?
            initializer = klass.methods.get('_%s_default' % trait_name)
            if initializer is not None:
                lineno    = initializer.lineno

            else:
                attribute = klass.attributes.get(trait_name)
                lineno    = attribute.lineno

        else:
            lineno = klass.lineno

        editor.select_line(lineno)

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_extension_trait(self, plugin, id):
        """ Return the extension trait with the specifed Id.

        Return None if the extension point was not declared via a trait.

        """

        extension_traits = plugin.traits(contributes_to=id)

        if len(extension_traits) > 0:
            # There is *at most* one extension point trait per extension point.
            trait_name = next(iter(extension_traits))

        else:
            trait_name = None

        return trait_name

    def _get_extension_point_trait(self, plugin, id):
        """ Return the extension point trait with the specifed Id.

        Return None if the extension point was not declared via a trait.

        """

        extension_point_traits = plugin.traits(__extension_point__=True)

        for trait_name, trait in extension_point_traits.items():
            if trait.trait_type.id == id:
                break

        else:
            trait_name = None

        return trait_name

    def _get_plugin(self, extension_point):
        """ Return the plugin that offered an extension point. """

        for plugin in self.application:
            if extension_point in plugin.get_extension_points():
                break

        else:
            plugin = None

        return plugin

    def _get_plugin_klass(self, module, plugin):
        """ Get the klass that defines the plugin. """

        for name, klass in module.klasses.items():
            if name == type(plugin).__name__:
                break

        else:
            klass = None

        return klass

    def _get_file_object(self, obj):
        """ Return a 'File' object for the object's source file. """

        return File(path=inspect.getsourcefile(type(obj)))

    def _parse_plugin(self, plugin):
        """ Parse the plugin source code. """

        filename = self._get_file_object(plugin).path

        return self.code_browser.read_file(filename)

#### EOF ######################################################################
