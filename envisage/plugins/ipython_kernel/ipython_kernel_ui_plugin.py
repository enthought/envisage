# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" An  IPython kernel plugin. """

# Enthought library imports.
from envisage.plugins.ipython_kernel.ipython_kernel_plugin import (
    IPYTHON_KERNEL_PROTOCOL)
from envisage.ui.tasks.api import TaskExtension
from envisage.api import Plugin
from traits.api import List
from pyface.tasks.action.api import SGroup, SchemaAddition


TASK_EXTENSIONS = 'envisage.ui.tasks.task_extensions'


class IPythonKernelUIPlugin(Plugin):
    """ Contributes UI actions on top of the IPython Kernel Plugin. """

    #### 'IPlugin' interface ##################################################

    # The plugin unique identifier.
    id = 'envisage.plugins.ipython_kernel_ui'

    # The plugin name (suitable for displaying to the user).
    name = 'IPython embedded kernel UI plugin'

    #### Contributions to extension points made by this plugin ################

    contributed_task_extensions = List(contributes_to=TASK_EXTENSIONS)

    #### Trait initializers ###################################################

    def _contributed_task_extensions_default(self):

        from .actions import StartQtConsoleAction

        def menu_factory():
            kernel = self.application.get_service(IPYTHON_KERNEL_PROTOCOL)
            return SGroup(
                StartQtConsoleAction(kernel=kernel),
                id='ipython'
            )

        return [
            TaskExtension(
                actions=[
                    SchemaAddition(
                        path='MenuBar/View',
                        factory=menu_factory,
                        id='IPythonSchema',
                    ),
                ]
            )
        ]
