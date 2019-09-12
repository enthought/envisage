# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" A collection of command-line tools for building encoded update.xml
files.
"""

class InfoFile:

    update_file = ""
    version = None
    checksum = None

    # A multi-line HTML document describing the changes between
    # this version and the previous version
    description = ""

    @classmethod
    def from_info_file(filename):
        return


def files2xml(filenames):
    """ Given a list of filenames, extracts the app version and log
    information from accompanying files produces an output xml file.

    There are no constraints or restrictions on the names or extensions
    of the input files.  They just need to be accompanied by a sidecar
    file named similarly, but with a ".info" extension, that can be
    loaded by the InfoFile class.
    """
    return



