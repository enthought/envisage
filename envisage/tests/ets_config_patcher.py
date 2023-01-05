# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import os
import shutil
import tempfile


class ETSConfigPatcher(object):
    """
    Object that patches the directories in ETSConfig, to avoid having
    tests write to the home directory.
    """

    def __init__(self):
        from traits.etsconfig.api import ETSConfig

        self.etsconfig = ETSConfig

        self.tmpdir = None
        self.old_application_data = None
        self.old_application_home = None
        self.old_user_data = None

    def start(self):
        tmpdir = self.tmpdir = tempfile.mkdtemp()

        self.old_application_data = self.etsconfig._application_data
        self.etsconfig._application_data = os.path.join(
            tmpdir, "application_data"
        )

        self.old_application_home = self.etsconfig._application_home
        self.etsconfig._application_home = os.path.join(
            tmpdir, "application_home"
        )

        self.old_user_data = self.etsconfig._user_data
        self.etsconfig._user_data = os.path.join(tmpdir, "user_home")

    def stop(self):
        if self.old_user_data is not None:
            self.etsconfig._user_data = self.old_user_data
            self.old_user_data = None

        if self.old_application_home is not None:
            self.etsconfig._application_home = self.old_application_home
            self.old_application_home = None

        if self.old_application_data is not None:
            self.etsconfig._application_data = self.old_application_data
            self.old_application_data = None

        if self.tmpdir is not None:
            shutil.rmtree(self.tmpdir)
            self.tmpdir = None
