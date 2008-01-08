""" Cookie action for plotting resources. """


# Major package imports.
from sets import Set

# Enthought library imports.
from enthought.envisage.project import CookieAction
from enthought.naming.api import Context
from enthought.pyface.api import OK
from enthought.pyface.new_dialog import NewDialog

# Local imports.
from enthought.plugins.chaco.cookie.plot_as_cookie import PlotAsCookie
from enthought.plugins.chaco.plotting_plugin import PlottingPlugin


class PlotAsCookieAction(CookieAction):
    """ Cookie action for plotting resources. """

    #### 'CookieAction' interface #############################################

    # Require the plot cookie to plot.
    required_cookie = PlotAsCookie

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self):
        """ Performs the action. """

        plugin = PlottingPlugin.instance

        from enthought.envisage import get_application
        from enthought.envisage.resource.resource_plugin import ResourcePlugin
        resource_manager = get_application().service_registry.get_service(
                  ResourcePlugin.IRESOURCE_MANAGER
            )

        # Get all the resource types for the selection.
        get_type_of = resource_manager.get_type_of
        resource_types = \
            Set([ get_type_of(binding.obj) for binding in self.window.selection ])

        # Get the template definitions for the selected resource types.
        template_definitions = \
            plugin.plot_template_manager.get_plot_templates(resource_types)

        # Let the user select a template for the selected resources.
        root = self._create_root_context(template_definitions)
        dialog = NewDialog(
            parent = self.window.control,
            root   = root,
            size   = (600, 400),
            style  = 'modal',
            text   = 'Choose a plot template',
            title  = 'Plot As',
        )

        if dialog.open() == OK:
            plot_factory = dialog.template
            plot_factory.create_plot_editor(self.window.selection,
                                            self.window)

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_root_context(self, template_description):
        """ Create a naming context for the template definitions. """

        root = Context()
        for description in template_description:
            # We must parse the full path name into the path and the name, so
            # that we can add the intermediate subcontexts along the path.
            pathname = description[0]
            components = pathname.split('/')
            if len(components) == 1:
                name = components[0]
                path = ''
            else:
                name = components[-1]
                path = '/'.join(components[:-1])

            # First, see if we already have the path context.
            try:
                context = root.lookup(path)

            # If not, create it.
            except:
                context = self._create_subcontext(path, root)

            # Bind the template factory in the context according to the name.
            context.rebind(name, description[1])

        return root

    def _create_subcontext(self, path, context):
        """ Create subcontexts in context along the path. """

        components = path.split('/')
        for dir in components:
            try:
                next_context = context.lookup(dir)
            except:
                next_context = context.create_subcontext(dir)

            context = next_context

        return context

#### EOF ######################################################################
