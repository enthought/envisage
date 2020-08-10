# (C) Copyright 2007-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

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
