# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
# Enthought library imports.
from traits.api import HasTraits, Instance, Vetoable

# Local imports.
from .task_window import TaskWindow


class TaskWindowEvent(HasTraits):
    """ A task window lifecycle event.
    """

    # The window that the event occurred on.
    window = Instance(TaskWindow)


class VetoableTaskWindowEvent(TaskWindowEvent, Vetoable):
    """ A vetoable task window lifecycle event.
    """

    pass
