# (C) Copyright 2007-2026 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
"""Tests for Envisage's logging setup."""

import logging
import unittest

import envisage  # noqa: F401 - imported for its side effects, if any.


class TestLogging(unittest.TestCase):
    """Tests for Envisage's logging setup."""

    def test_no_handler_on_the_envisage_logger(self):
        """the 'envisage' logger has no handler of its own"""

        # Envisage deliberately doesn't install a handler - not even a
        # NullHandler - on its top-level logger. A NullHandler would stop
        # records propagating to logging.lastResort, and so would hide
        # Envisage's warnings and errors from applications that haven't
        # configured logging themselves. See enthought/envisage#574.
        self.assertEqual([], logging.getLogger("envisage").handlers)
