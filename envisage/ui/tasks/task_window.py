# Enthought library imports.
from pyface.tasks.api import TaskWindow as PyfaceTaskWindow
from traits.api import Instance, Property, Unicode


class TaskWindow(PyfaceTaskWindow):
    """ A TaskWindow for use with the Envisage Tasks plugin.
    """

    # The application that created and is managing this window.
    application = Instance('envisage.ui.tasks.api.TasksApplication')

    ###########################################################################
    # Protected 'TaskWindow' interface.
    ###########################################################################

    def _get_title(self):
        """ If the application has a name, add it to the title. Otherwise,
            behave like the base class.
        """
        if self._title or self.active_task is None:
            return self._title

        title = self.active_task.name
        if self.application.name:
            title = u'%s - %s' % (title, self.application.name)
        return title
