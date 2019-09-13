# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
"""
Tests for the envisage.__version__ attribute and the envisage.version
module contents.
"""

from __future__ import absolute_import, print_function, unicode_literals

import unittest

import pkg_resources
import six

import envisage


class TestVersion(unittest.TestCase):
    def test_dunder_version(self):
        self.assertIsInstance(envisage.__version__, six.text_type)
        # Round-trip through parse_version; this verifies not only
        # that the version is valid, but also that it's properly normalised
        # according to the PEP 440 rules.
        parsed_version = pkg_resources.parse_version(envisage.__version__)
        self.assertEqual(six.text_type(parsed_version), envisage.__version__)

    def test_version_version(self):
        # Importing inside the test to ensure that we get a test error
        # in the case where the version module does not exist.
        from envisage.version import version

        self.assertIsInstance(version, six.text_type)
        parsed_version = pkg_resources.parse_version(version)
        self.assertEqual(six.text_type(parsed_version), version)

    def test_version_git_revision(self):
        from envisage.version import git_revision

        self.assertIsInstance(git_revision, six.text_type)

        # Check the form of the revision. Could use a regex, but that seems
        # like overkill.
        self.assertEqual(len(git_revision), 40)
        self.assertLessEqual(set(git_revision), set("0123456789abcdef"))

    def test_versions_match(self):
        import envisage.version

        self.assertEqual(envisage.version.version, envisage.__version__)
