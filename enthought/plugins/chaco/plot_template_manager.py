""" Manages bindings from resource types to PlotDataFactory's. """


# Enthought library imports.
from enthought.envisage import get_application
from enthought.traits.api import Dict, HasPrivateTraits

# Plugin imports.
from enthought.plugins.chaco.cookie.plot_as_cookie import PlotAsCookie


class PlotTemplateManager(HasPrivateTraits):
    """ Manages bindings from resource types to PlotDataFactory's. """

    #### Trait definitions ####################################################

    # FIXME: This currently stores tuples which makes unregistering pretty
    #        hackish...
    template_map = Dict


    ###########################################################################
    # 'PlotDataManager' interface.
    ###########################################################################


    def register_template(self, template_factory, resource_types, name):
        """ Register a template factory.

        resource_types is a list of resource types for which the template is
        available.

        category is the category where the template will be shown to the user.

        name is the name of the template that will be shown to the user.
        """

        from enthought.envisage.resource.resource_ui_plugin import ResourceUIPlugin
        cookie_manager = get_application().get_service(
                  ResourceUIPlugin.ICOOKIE_MANAGER
            )

        for resource_type in resource_types:
            # Add the template definition to the list of templates for the
            # resource type.
            templates = self.template_map.setdefault(resource_type, [])
            templates.append((name, template_factory))

            # Since we have at least one template for this resource type,
            # add the PlotAsCookie to the resource type.
            cookie_manager.add_type_cookie(
                PlotAsCookie, PlotAsCookie(), resource_type
            )

        return

    def unregister_template(self, resource_types, name):
        """ Unregister a template factory. """

        for resource_type in resource_types:
            templates = self.template_map.get(resource_type, [])
            remaining_templates = [template for template in templates if \
                                   template[0] != name]

            # If there are no more templates for this resource type, we need
            # to remove the PlotAsCookie and also clean up our template map.
            if len(remaining_templates) == 0:
                del self.template_map[resource_type]
                cookie_manager.remove_type_cookie(PlotAsCookie, type)

            # Otherwise, we just need to clean up our template map.
            self.template_map[resource_type] = remaining_templates

            return

    def get_plot_templates(self, resource_types):
        """ Get all of the template definitions for the resource type. """

        result = []
        for resource_type in resource_types:
            result.extend(self.template_map.get(resource_type, []))

        return result

#### EOF ######################################################################



