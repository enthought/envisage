# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

# Enthought library imports.
from pyface.image_resource import ImageResource
from pyface.tasks.api import TaskWindow as PyfaceTaskWindow
from traits.api import Instance, Property

# Local imports.
from envisage._compat import unicode_str


class TaskWindow(PyfaceTaskWindow):
    """ A TaskWindow for use with the Envisage Tasks plugin.
    """

    # The application that created and is managing this window.
    application = Instance('envisage.ui.tasks.api.TasksApplication')

    # The window's icon.  We override it so it can delegate to the application
    # icon if the window's icon is not set.
    icon = Property(Instance(ImageResource), depends_on='_icon')

    #### Protected interface ##################################################

    _icon = Instance(ImageResource, allow_none=True)

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
            form = unicode_str('%s - %s')
            title = form % (title, self.application.name)
        return title

    def _get_icon(self):
        """If we have an icon return it, else delegate to the application.
        """
        if self._icon is not None:
            return self._icon
        elif self.application is not None:
            return self.application.icon
        else:
            return None

    def _set_icon(self, icon):
        """Explicitly set the icon to use.  None is allowed.
        """
        self._icon = icon
