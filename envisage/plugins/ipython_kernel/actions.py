from pyface.tasks.action.api import TaskAction
from traits.api import Instance

from .internal_ipkernel import InternalIPKernel


class StartQtConsoleAction(TaskAction):

    id = 'ipython_qtconsole'

    name = 'Console'

    kernel = Instance(InternalIPKernel)

    def perform(self, event=None):

        self.kernel.new_qt_console()


