

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
