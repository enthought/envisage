""" The plotting plugin. """


# Enthought library imports.
from enthought.envisage import get_application, Plugin
from enthought.traits.api import Instance

# Plugin definition imports.
from plot_data_manager import PlotDataManager
from plot_template_manager import PlotTemplateManager
from plotting_plugin_definition import PlotDataFactories, PlotTemplateFactories

class PlottingPlugin(Plugin):
    """ The plotting plugin. """

    # The shared plugin instance.
    instance = None

    # The plot data manager.
    plot_data_manager = Instance(PlotDataManager, ())

    plot_template_manager = Instance(PlotTemplateManager, ())

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **kw):
        """ Creates a new plugin. """

        # Base class constructor.
        super(PlottingPlugin, self).__init__(**kw)

        # Set the shared instance.
        PlottingPlugin.instance = self

        return

    ###########################################################################
    # 'Plugin' interface.
    ###########################################################################

    def start(self, application):
        """ Starts the plugin. """

        import_manager = application.import_manager
        from enthought.envisage.resource.resource_plugin import ResourcePlugin
        resource_manager = application.service_registry.get_service(
                  ResourcePlugin.IRESOURCE_MANAGER
            )

## None of this is tested or working, so I'm commenting it out.  FIXME
##         id = PlotDataFactories
##         extensions = application.extension_registry.get_extensions(id)
##         for factory_defintion in extensions:
##             # Register the PlotDataFactory with the PlotDataManager
##             plot_data_factory = self._create_instance(
##                 factory_defintion.class_name
##             )

##             for resource_type_class_name in factory.resource_types:
##                 self._bind_resource(resouce_type_class_name, plot_data_factory)

        id = PlotTemplateFactories
        extensions = application.extension_registry.get_extensions(id)
        template_manager = self.plot_template_manager
        for extension in extensions:
            for factory_definition in extension.factories:

                # Create the factory and register it with the template manager.
                factory = self._create_instance(factory_definition.class_name)
                resource_types = [ resource_manager.lookup(resource_type) for resource_type in factory_definition.resource_types ]
                template_manager.register_template(
                    factory, resource_types,
                    '/'.join((factory_definition.category, factory_definition.name))
                )

        return

    def stop(self, application):
        """ Stops the plugin. """

        pass

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _bind_resource(self, resource_type_class_name, plot_data_factory):
        """ Bind a named resource type to a plot data factory. """

        resource_type = self._create_instance(resource_type_class_name)
        self.plot_data_manager.bind_resource(resource_type, plot_data_factory)

        return

    def _create_instance(self, class_name):
        """ Create an instance of the named class. """

        import_manager = get_application().import_manager

        klass = import_manager.import_symbol(class_name)
        return klass()

#### EOF ######################################################################
