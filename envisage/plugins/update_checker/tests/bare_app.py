# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!


# Standard library imports.
import logging

# Enthought library imports.
from envisage.ui.workbench.api import WorkbenchApplication
from envisage.core_plugin import CorePlugin
from envisage.ui.workbench.workbench_plugin import WorkbenchPlugin
from enthought.epdlab.plugins.code_editor.plugin import CodeEditorPlugin

# Logging.
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(open('update_checker.log', 'w')))
logger.setLevel(logging.DEBUG)


def main():
    application = Application(
        id='Update Checker Tester', plugins=[UpdateChecker()]
    )

    application = WorkbenchApplication(
        id='update_checker_tester', name='Update Checker',
        plugins=[
            CorePlugin(),
            WorkbenchPlugin(),
            UpdateCheckerPlugin(

                ),
        ])
    application.run()

if __name__ == "__main__":
    main()
