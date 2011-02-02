# Enthought library imports.
from enthought.pyface.tasks.api import TaskWindow as PyfaceTaskWindow
from enthought.traits.api import Instance


class TaskWindow(PyfaceTaskWindow):
    """ A TaskWindow for use with the Envisage Tasks plugin.
    """

    # The application that created and is managing this window.
    application = Instance('enthought.envisage.ui.tasks.api.TasksApplication')
