"""Compatibility layer for Python version 2.x and 3.x.
"""

import sys

PY_VER = sys.version_info[0]

if PY_VER >= 3:
    import pickle
    from urllib.request import urlopen
    from urllib.error import HTTPError
    STRING_BASE_CLASS = str
else:
    import cPickle as pickle
    from urllib2 import urlopen, HTTPError
    STRING_BASE_CLASS = basestring

def unicode_str(x=''):
    return str(x) if PY_VER == 3 else unicode(x, encoding='utf-8')
