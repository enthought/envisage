""" The Lorenz UI plugin. """


# Enthought library imports.
from envisage.api import Plugin
from pyface.workbench.api import Perspective, PerspectiveItem
from pyface.workbench.api import TraitsUIView
from traits.api import List


class LorenzPerspective(Perspective):
    """ A perspective containing the default Lorenz views. """

    name             = 'Lorenz'
    show_editor_area = False

    contents = [
        PerspectiveItem(id='lorenz.data'),
        PerspectiveItem(id='lorenz.plot2d')
    ]


class LorenzUIPlugin(Plugin):
    """ The Lorenz UI plugin.

    This plugin is part of the 'Lorenz' example application.

    """

    # Extension points Ids.
    PERSPECTIVES   = 'envisage.ui.workbench.perspectives'
    VIEWS          = 'envisage.ui.workbench.views'

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'acme.lorenz.ui'

    # The plugin's name (suitable for displaying to the user).
    name = 'Lorenz UI'

    #### Contributions to extension points made by this plugin ################

    # Perspectives.
    perspectives = List(contributes_to=PERSPECTIVES)

    def _perspectives_default(self):
        """ Trait initializer. """

        return [LorenzPerspective]

    # Views.
    views = List(contributes_to=VIEWS)

    def _views_default(self):
        """ Trait initializer. """

        return [self._create_data_view, self._create_plot2d_view]

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_data_view(self, **traits):
        """ Factory method for the data view. """

        from acme.lorenz.api import DataView, Lorenz

        data_view = TraitsUIView(
            id   = 'lorenz.data',
            name = 'Data',
            obj  = DataView(lorenz=self.application.get_service(Lorenz)),
            **traits
        )

        return data_view

    def _create_plot2d_view(self, **traits):
        """ Factory method for the plot2D view. """

        from acme.lorenz.api import Lorenz, Plot2DView

        plot2d_view = TraitsUIView(
            id   = 'lorenz.plot2d',
            name = 'Plot 2D',
            obj  = Plot2DView(lorenz=self.application.get_service(Lorenz)),
            **traits
        )

        return plot2d_view

#### EOF ######################################################################
