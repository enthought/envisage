# Copyright (c) 2007-2015 by Enthought, Inc.
# All rights reserved.

try:
    from envisage.version import version as __version__
except ImportError:
    # If we get here, we're using a source tree that hasn't been created via
    # the setup script.
    __version__ = "unknown"

# Per logging best practices, add a NullHandler to the root 'envisage'
# logger.
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

del logging
