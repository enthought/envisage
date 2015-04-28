# Copyright (c) 2007-2015 by Enthought, Inc.
# All rights reserved.

from ._version import full_version as __version__  # noqa

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
