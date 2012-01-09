""" A UI for browsing a plugin. """


# Enthought library imports.
from envisage.api import ExtensionPoint, IPlugin
from traits.api import Delegate, HasTraits, Instance, List, Property
from traits.api import Code, Str
from traitsui.api import Item, TableEditor, View, VGroup
from traitsui.table_column import ObjectColumn # fixme: non-api!

class ExtensionPointModel(Hastraits):
    """ A model for browsing an extension point. """

    # The plugin that offered the extension point.
    plugin = Instance(IPlugin)

    # The extension point.
    extension_point = Instance(IExtensionPoint)

    #### 'ExtensionPointModel' interface ######################################



class ExtensionModel(Hastraits):
    """ A model for browsing a contribution to an extension point. """

    # The plugin that made the contribution.
    plugin = Instance(IPlugin)

    #### 'ContributionModel' interface ########################################

    # The Id of the extension point that the contribution is for.
    extension_point_id = Str

    # The contributions to the extension point.
    contributions = List

    ###########################################################################
    # 'ApplicationModel' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _contributions_default(self):
        """ Trait initializer. """

        return plugin.application.get_extensions(self.extension_point_id)


class PluginModel(HasTraits):
    """ A model for browsing a plugin.  """

    # The plugin that we are a model for.
    plugin = Instance(IPlugin)

    #### 'PluginModel' interface ##############################################

    # Models for each of the plugin's extension points.
    extension_point_models = List(ExtensionPointModel)

    # Models for each of the plugin's contributions to extension points.
    extension_models = List(ExtensionModel)

    ###########################################################################
    # 'ApplicationModel' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _extension_models_default(self):
        """ Trait initializer. """

        extension_models = [
            ExtensionModel(
                plugin             = plugin,
                extension_point_id = extension_point.id
            )

            for extension_point in plugin.get_extension_points()
        ]

        return extension_models

    def _extension_point_models_default(self):
        """ Trait initializer. """

        extension_point_models = [
            ExtensionPointModel(
                plugin          = plugin,
                extension_point = extension_point
            )

            for extension_point in plugin.get_extension_points()
        ]

        return extension_point_models


class ApplicationModel(HasTraits):
    """ A model for browsing an application. """

    # The application that we are a model for.
    application = Instance(IApplication)

    #### 'ApplicationModel' interface #########################################

    # Models for each of the application's plugins.
    plugin_models = List(PluginModel)

    ###########################################################################
    # 'ApplicationModel' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _plugin_models_default(self):
        """ Trait initializer. """

        return [PluginModel(plugin=plugin) for plugin in self.application]



extension_point_table_editor = TableEditor(
    columns = [
        ObjectColumn(name='id'),
        #ObjectColumn(name='desc')
    ],

#   selected = 'extension_point_selected',
    editable  = True,
    edit_view = View(Item(name='desc', show_label=False), style='custom')
)

plugin_browser_view = View(
    VGroup(
        Item(name='id'),
        Item(name='name'),
        label='General'
    ),

    VGroup(
        Item(
            name       = 'extension_points',
            editor     = extension_point_table_editor,
            show_label = False
        ),

        label='Extension Points',
    ),

    width  = .8,
    height = .6
)


class ExtensionPointBrowser(HasTraits):
    """ The model used to view extension points.

    This browser is required because 'ExatenionPoint' instances are trait
    *types* and therefore do not have traits themselves and so this class is
    really just a 'traitified' wrapper.

    """

    #### 'ExtensionPointBrowser' interface ####################################

    # The extension point that we are browsing.
    extension_point = Instance(ExtensionPoint)

    # The extension point's globally unique Id.
    id = Str

    # The extension point's description.
    desc = Code#Str

    ###########################################################################
    # 'ExtensionPoint' browser interface.
    ###########################################################################

    def _id_default(self):
        """ Trait initializer. """

        return self.extension_point.id

    def _desc_default(self):
        """ Trait initializer. """

        desc = self.extension_point.desc.strip()

        lines = [line.replace('    ', '', 2) for line in desc.splitlines()]

        return '\n'.join(lines)


# Convenience trait to delegate an attribute to a plugin.
DelegatedToPlugin = Delegate('plugin', modify=True)


class PluginBrowser(HasTraits):
    """ A plugin browser.

    Actually, this class exists just because to use a trait editor we have
    to have a trait to edit!

    """

    #### 'IPlugin' interface ##################################################

    # The plugins Id.
    id = DelegatedToPlugin

    # The plugin name.
    name = DelegatedToPlugin

    #### 'PluginBrowser' interface ############################################

    # The extension points offered by the plugin.
    extension_points = Property(List)

    # The plugin that we are browsing.
    plugin = Instance(IPlugin)

    # The default traits UI view.
    traits_view = plugin_browser_view

    ###########################################################################
    # 'PluginBrowser' interface.
    ###########################################################################

    def _get_extension_points(self):
        """ Property getter. """

        extension_points = [
            ExtensionPointBrowser(extension_point=extension_point)

            for extension_point in self.plugin.extension_points
        ]

        return extension_points


def browse_plugin(plugin):
    """ Browse a plugin. """

    import inspect

    if inspect.isclass(plugin):
        plugin = plugin()

    plugin_browser = PluginBrowser(plugin=plugin)
    plugin_browser.configure_traits(view=plugin_browser_view)

    return

#### EOF ######################################################################
