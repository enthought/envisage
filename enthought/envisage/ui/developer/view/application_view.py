""" A view showing a summary of the running application. """


# Enthought library imports.
from enthought.pyface.workbench.api import TraitsUIView

# Local imports.
from application_browser import ApplicationBrowser


class ApplicationView(TraitsUIView):
    """ A view showing a summary of the running application. """

    #### 'IWorkbenchPart' interface ###########################################
    
    # The part's globally unique identifier.
    id = 'enthought.envisage.ui.developer.view.application_view'

    # The part's name (displayed to the user).
    name = 'Application'

    ###########################################################################
    # 'TraitsUIView' interface.
    ###########################################################################

    def _model_default(self):
        """ Trait initializer. """

        return ApplicationBrowser(application=self.window.application)
    
##     def _model_default(self):
##         """ Trait initializer. """

##         from enthought.traits.ui.value_tree import ObjectNode
##         value = ObjectNode(value=self.window.application))

##         return ApplicationBrowser(value=value)

#### EOF ######################################################################
