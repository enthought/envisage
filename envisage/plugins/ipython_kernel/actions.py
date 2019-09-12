# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
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
