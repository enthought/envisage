""" An implementation of weak references that works for bound methods.

This code is based on the code in the Python Cookbook, but you can call `ref`
for objects that are *not* bound methods too, in which case it just returns a
standard `weakref.ref`.

Weak references to bound methods are cached so that `ref(x) is ref(x)` as for
standard weakrefs, and the `ref` class defined here is therefore intended to be
used as a drop-in replacement for 'weakref.ref'.

"""


# Standard library imports.
import sys
import types
#import new
import weakref

# Because this module is intended as a drop-in replacement for weakref, we
# import everything from that module here (so the user can do things like
# "import safeweakref as weakref" etc).
from weakref import *


class ref(object):
    """ An implementation of weak references that works for bound methods. """

    # A cache containing the weak references we have already created.
    #
    # We cache the weak references by the object containing the associated
    # bound methods, hence this is a dictionary of dictionaries in the form:-
    #
    # { bound_method.__self__ : { bound_method.__func__ : ref } }
    #
    # This makes sure that when the object is garbage collected, any cached
    # weak references are garbage collected too.
    _cache = weakref.WeakKeyDictionary()

    def __new__(cls, obj, *args, **kw):
        """ Create a new instance of the class. """

        # If the object is a bound method then either get from the cache, or
        # create an instance of *this* class.
        if hasattr(obj, '__self__'):
            func_cache = ref._cache.setdefault(obj.__self__, {})

            # If we haven't created a weakref to this bound method before, then
            # create one and cache it.
            self = func_cache.get(obj.__func__)
            if self is None:
                if sys.version_info[0] > 2:
                    self = object.__new__(cls)
                else:
                    self = object.__new__(cls, obj, *args, **kw)
                func_cache[obj.__func__] = self

        # Otherwise, just return a regular weakref (because we aren't
        # returning an instance of *this* class our constructor does not get
        # called).
        else:
            self = weakref.ref(obj)

        return self

    def __init__(self, obj):
        """ Create a weak reference to a bound method object.

        'obj' is *always* a bound method because in the '__new__' method we
        don't return an instance of this class if it is not, and hence this
        constructor doesn't get called.

        """

        self._cls = obj.__self__.__class__
        self._fn  = obj.__func__
        self._ref = weakref.ref(obj.__self__)

        return

    def __call__(self):
        """ Return a strong reference to the object.

        Return None if the object has been garbage collected.

        """

        obj = self._ref()
        if obj is not None:
            obj = types.MethodType(self._fn, obj)

        return obj

#### EOF ######################################################################
