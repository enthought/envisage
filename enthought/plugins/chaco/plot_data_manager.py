""" Manages bindings from resource types to PlotDataFactory's. """

# Enthought library imports.
from enthought.envisage.project import CookieManager
from enthought.traits.api import Dict, HasPrivateTraits

# Local imports.
from exception import ResourceAlreadyBoundError, ResourceNotFoundError
from enthought.plugins.chaco.cookie.plot_cookie import PlotCookie

class PlotDataManager(HasPrivateTraits):
    """ Manages bindings from resource types to PlotDataFactory's. """

    #### Trait definitions ####################################################

    bindings = Dict


    ###########################################################################
    # 'PlotDataManager' interface.
    ###########################################################################

    def bind_resource(self, resource, plot_data_factory):
        """ Bind the PlotDataFactory to the Resource.

        As a side effect, a PlotDataCookie is attached to the resource, so it
        will be plottable.
        """

        from plot_data_cookie import PlotDataCookie
        # Only allow one binding per resource type.
        if self.bindings.has_key(resource):
            raise ResourceAlreadyBoundError(str(resource))

        else:
            self.bindings[resource] = plot_data_factory

            # Add the PlotDataCookie to make the resource "plottable".
            cookie_manager = CookieManager()
            cookie_manager.add_type_cookie(
                PlotCookie, PlotDataCookie(), resource
            )

        return

##     def unbind_resource(self, resource):
##         """ Unbind the PlotDataFactory from the Resource. """

##         from plot_data_cookie import PlotDataCookie
##         if self.bindings.has_key(resource):
##             del self.bindings[resource]

##             # Remove the PlotDataCookie to make the resource "unplottable".
##             cookie_manager = CookieManager()
##             cookie_manager.unbind_resource(resource, PlotDataCookie())

##         else:
##             raise ResourceNotFoundError(str(resource))

##         return

    def get_plot_data_factory(self, resource):
        """ Get the PlotDataFactory for the resource. """

        if self.bindings.has_key(resource):
            result = self.bindings[resource]

        else:
            raise ResourceNotFoundError(str(resource))

        return result

#### EOF ######################################################################



