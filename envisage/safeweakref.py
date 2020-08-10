# (C) Copyright 2007-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" An implementation of weak references that works for bound methods.

This code is based on the code in the Python Cookbook, but you can call `ref`
for objects that are *not* bound methods too, in which case it just returns a
standard `weakref.ref`.

Weak references to bound methods are cached so that `ref(x) is ref(x)` as for
standard weakrefs, and the `ref` class defined here is therefore intended to be
used as a drop-in replacement for 'weakref.ref'.

"""

# Standard library imports.
import warnings
import weakref


class ref(object):
    """An implementation of weak references that works for bound methods and
    caches them.

    If ``object`` is a bound method, returns a ``weakref.WeakMethod`` for that
    method. This ensures that the method is kept alive for the lifetime of the
    object that it's bound to.

    For any other ``object``, a normal ``weakref.ref`` is returned.

    .. deprecated:: 5.0.0

    """
    _cache = weakref.WeakKeyDictionary()

    def __new__(cls, obj, callback=None):
        warnings.warn(
            message=(
                "safeweakref.ref is deprecated, and will be removed in a "
                "future version of Envisage"
            ),
            category=DeprecationWarning,
            stacklevel=2,
        )

        if getattr(obj, "__self__", None) is not None:  # Bound method
            # Caching
            func_cache = cls._cache.setdefault(obj.__self__, {})
            self = func_cache.get(obj.__func__)
            if self is None:
                self = weakref.WeakMethod(obj, callback)
                func_cache[obj.__func__] = self
            return self
        else:
            return weakref.ref(obj, callback)
