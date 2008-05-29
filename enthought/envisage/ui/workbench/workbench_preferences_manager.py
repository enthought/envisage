""" The preferences manager for the workbench. """


# Enthought library imports.
from enthought.preferences.ui.api import PreferencesManager
from enthought.traits.api import Callable, List


class WorkbenchPreferencesManager(PreferencesManager):
    """ The preferences manager for the workbench.

    The only difference between this and the base class is that it uses
    factories to create its preferences pages. The factories are simply
    callables with the following signature::

        callable() -> IPrefrerencesPage

    """

    #### 'WorkbenchPreferencesManager' interface ##############################

    # Factories for the actual preferences pages.
    page_factories = List(Callable)

    ###########################################################################
    # 'PreferencesManager' interface.
    ###########################################################################

    def _pages_default(self):
        """ Trait initializer. """

        return [page_factory() for page_factory in self.page_factories]
    
#### EOF ######################################################################
