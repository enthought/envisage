# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" A non-GUI application with a twisted reactor event loop.

Nothing is imported from twisted until the application is started so this
module can safely live in the Envisage core without twisted being installed.

"""


# Standard library imports.
import logging

# Enthought library imports.
from envisage.api import Application


# Logging.
logger = logging.getLogger(__name__)


class TwistedApplication(Application):
    """ A non-GUI application with a twisted reactor event loop. """

    def start(self):
        """ Start the application. """

        started = super(TwistedApplication, self).start()

        # Don't start the event loop if the start was vetoed.
        if started:
            from twisted.internet import reactor

            logger.debug('---------- reactor starting ----------')
            reactor.run()

        return started

    def stop(self):
        """ Stop the application. """

        stopped = super(TwistedApplication, self).stop()

        # Don't stop the event loop if the stop was vetoed.
        if stopped:
            from twisted.internet import reactor

            logger.debug('---------- reactor stopping ----------')
            reactor.stop()

        return stopped

#### EOF ######################################################################
