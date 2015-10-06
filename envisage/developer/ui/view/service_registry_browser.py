""" A view showing a summary of the running application. """


# Standard library imports.
import inspect

# Enthought library imports.
from envisage.api import IApplication, IExtensionPoint
from envisage.api import IServiceRegistry
from envisage.developer.code_browser.api import CodeBrowser
from apptools.io.api import File
from traits.api import Any, HasTraits, Instance
from traitsui.api import Item, TreeEditor, View

# fixme: non-api import.
from envisage.plugins.text_editor.editor.text_editor import TextEditor

# Local imports.
from .service_registry_browser_tree import \
     service_registry_browser_tree_nodes


service_registry_browser_view = View(
    Item(
        name       = 'service_registry_model',
        show_label = False,
        editor     = TreeEditor(
            nodes       = service_registry_browser_tree_nodes,
            editable    = False,
            orientation = 'vertical',
            hide_root   = True,
            show_icons  = True,
            on_dclick   = 'object.dclick'
        )
    ),

    resizable = True,
    style     = 'custom',
    title     = 'Service Registry',

    width     = .1,
    height    = .1
)


class ServiceRegistryBrowser(HasTraits):
    """ An extension registry browser.

    Actually, this class exists just because to use a trait editor we have
    to have a trait to edit!

    """

    #### 'ServiceRegistryBrowser' interface #################################

    # The application that whose extension registry we are browsing.
    application = Instance(IApplication)

    # The code browser that we use to parse plugin source code.
    code_browser = Instance(CodeBrowser)

    # The extension registry that we are browsing.
    service_registry = Instance(IServiceRegistry)

    # The extension registry that we are browsing.
    service_registry_model = Any#Instance(IServiceRegistry)

    # The workbench service.
    workbench = Instance('envisage.ui.workbench.api.Workbench')

    # The default traits UI view.
    traits_view = service_registry_browser_view

    ###########################################################################
    # 'ServiceRegistryBrowser' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _service_registry_default(self):
        """ Trait initializer. """

        return self.application.service_registry

    def _service_registry_model_default(self):
        """ Trait initializer. """

        from .service_registry_browser_tree import ServiceRegistryModel

        return ServiceRegistryModel(service_registry=self.service_registry)

    def _workbench_default(self):
        """ Trait initializer. """

        workbench = self.application.get_service(
            'envisage.ui.workbench.workbench.Workbench'
        )

        return workbench

    #### Methods ##############################################################

    def dclick(self, obj):
        """ Called when an object in the tree is double-clicked. """

        if hasattr(obj, '_service_id_'):
            protocol = obj._protocol_
            id       = obj._service_id_
            service  = obj.value

            for plugin in self.application:
                if id in plugin._service_ids:
                    self.dclick_service(plugin, protocol, service)
                    break

            else:
                self.workbench.information(
                    'Service not created by a plugin (%s)' % repr(service)
                )

        return

    def dclick_service(self, plugin, protocol, obj):
        """ Called when an extension is double-clicked. """

        # Parse the plugin source code.
        module = self._parse_plugin(plugin)

        # Get the plugin klass.
        klass = self._get_plugin_klass(module, plugin)

        # Edit the plugin.
        editor = self.workbench.edit(
            self._get_file_object(plugin), kind=TextEditor
        )

        # Was the service offered declaratively?
        trait_name = self._get_service_trait(plugin, protocol, obj)
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

    def _get_service_trait(self, plugin, protocol, obj):
        """ Return the servicetrait with the specifed Id.

        Return None if the service was not declared via a trait.

        """

        service_traits = plugin.traits(service=True)

        protocol = self.application.import_symbol(protocol)

        for trait_name, trait in service_traits.items():
            if protocol == self._get_service_protocol(trait):
                break

        else:
            trait_name = None

        return trait_name

    def _get_service_protocol(self, trait):
        """ Determine the protocol to register a service trait with. """

        # If a specific protocol was specified then use it.
        if trait.service_protocol is not None:
            protocol = trait.service_protocol

        # Otherwise, use the type of the objects that can be assigned to the
        # trait.
        #
        # fixme: This works for 'Instance' traits, but what about 'AdaptsTo'
        # and 'AdaptedTo' traits?
        else:
            # Note that in traits the protocol can be an actual class or
            # interfacem or the *name* of a class or interface. This allows
            # us to lazy load them!
            protocol = trait.trait_type.klass

        return protocol

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
