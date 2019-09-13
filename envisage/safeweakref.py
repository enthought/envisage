# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
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
import sys, weakref

# Because this module is intended as a drop-in replacement for weakref, we
# import everything from that module here (so the user can do things like
# "import safeweakref as weakref" etc).

from weakref import *

__all__ = weakref.__all__

if hasattr(weakref, "WeakMethod"):
    pass
else:
    # Backport WeakMethod from Python 3
    class WeakMethod(weakref.ref):
        """
        A custom `weakref.ref` subclass which simulates a weak reference to
        a bound method, working around the lifetime problem of bound methods.
        """

        __slots__ = "_func_ref", "_meth_type", "_alive", "__weakref__"

        def __new__(cls, meth, callback=None):
            try:
                obj = meth.__self__
                func = meth.__func__
            except AttributeError:
                raise TypeError(
                    "argument should be a bound method, not {}"
                    .format(type(meth))
                )
            def _cb(arg):
                # The self-weakref trick is needed to avoid creating a reference
                # cycle.
                self = self_wr()
                if self._alive:
                    self._alive = False
                    if callback is not None:
                        callback(self)
            self = weakref.ref.__new__(cls, obj, _cb)
            self._func_ref = weakref.ref(func, _cb)
            self._meth_type = type(meth)
            self._alive = True
            self_wr = weakref.ref(self)
            return self

        def __call__(self):
            obj = weakref.ref.__call__(self)
            func = self._func_ref()
            if obj is None or func is None:
                return None
            return self._meth_type(func, obj)

        def __eq__(self, other):
            if isinstance(other, WeakMethod):
                if not self._alive or not other._alive:
                    return self is other
                return weakref.ref.__eq__(self, other) and self._func_ref == other._func_ref
            return False

        def __ne__(self, other):
            if isinstance(other, WeakMethod):
                if not self._alive or not other._alive:
                    return self is not other
                return weakref.ref.__ne__(self, other) or self._func_ref != other._func_ref
            return True

        __hash__ = weakref.ref.__hash__


class ref(object):
    """ An implementation of weak references that works for bound methods and \
    caches them. """
    _cache = weakref.WeakKeyDictionary()

    def __new__(cls, obj, callback=None):
        if getattr(obj, "__self__", None) is not None:  # Bound method
            # Caching
            func_cache = cls._cache.setdefault(obj.__self__, {})
            self = func_cache.get(obj.__func__)
            if self is None:
                self = WeakMethod(obj, callback)
                func_cache[obj.__func__] = self
            return self
        else:
            return weakref.ref(obj, callback)

#### EOF ######################################################################
