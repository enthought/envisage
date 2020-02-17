# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
"""Compatibility layer for Python version 2.x and 3.x.
"""

import sys

PY_VER = sys.version_info[0]

if PY_VER >= 3:
    import pickle
else:
    import cPickle as pickle
