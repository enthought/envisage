# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

import unittest

import six

import envisage.ids


class TestIds(unittest.TestCase):
    def test_envisage_extension_points(self):
        extension_point_ids = [
            "PREFERENCES",
            "SERVICE_OFFERS",
            "BINDINGS",
            "COMMANDS",
            "IPYTHON_NAMESPACE",
            "IPYTHON_KERNEL_PROTOCOL",
            "PREFERENCES_CATEGORIES",
            "PREFERENCES_PANES",
            "TASKS",
            "TASK_EXTENSIONS",
        ]

        for extension_point_id in extension_point_ids:
            id_value = getattr(envisage.ids, extension_point_id)
            self.assertIsInstance(id_value, six.string_types)
