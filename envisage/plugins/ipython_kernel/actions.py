from pyface.tasks.action.api import TaskAction
from traits.api import Instance

from .internal_ipkernel import InternalIPKernel


class StartQtConsoleAction(TaskAction):
    """ Open in a separate window a Qt console attached to a, existing kernel.
    """

    id = 'ipython_qtconsole'

    name = 'IPython Console'

    kernel = Instance(InternalIPKernel)

    def perform(self, event=None):
        self.kernel.new_qt_console()
