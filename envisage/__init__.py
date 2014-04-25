# Copyright (c) 2007-2013 by Enthought, Inc.
# All rights reserved.

__version__ = '4.5.0.dev'

__requires__ = [
    'apptools',
    'traits',
]

# Per logging best practices, add a NullHandler to the root 'envisage'
# logger.
import logging


class NullHandler(logging.Handler):
    # Define our own to accommodate Python < 2.7
    def handle(self, record):
        pass

    def emit(self, record):
        pass

    def createLock(self):
        self.lock = None


logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())

del logging, logger, NullHandler
