""" An implementation of weak references that works for bound methods.

This code is based on the code in the Python Cookbook, but uses weak references
for everything that is *not* a bound method too. It also adds comparison and
hash methods to allow the weak references to be compared just like standard
weak references. It is therefore intended to be used as a drop-in replacement
for 'weakref.ref'.

"""


# Standard library imports.
import new, weakref


class ref(object):
    """ An implementation of weak references that works for bound methods. """

    def __init__(self, obj):
        """ Create a weak reference to an object. """

        # Is the object a bound method?
        if hasattr(obj, 'im_self'):
            self._cls = obj.im_class
            self._fn  = obj.im_func
            self._ref = weakref.ref(obj.im_self)

        # Otherwise, it is an arbitrary object (unbound methods and plain ol'
        # functions fall into this category too!).
        else:
            self._cls = None
            self._fn  = None
            self._ref = weakref.ref(obj)

        return

    def __call__(self):
        """ Return a strong reference to the object.

        Return None if the object has been garbage collected.

        """

        obj = self._ref()
        if obj is not None and self._cls is not None:
            obj = new.instancemethod(self._fn, obj, self._cls)

        return obj

    def __cmp__(self, other):
        """ Compare two objects. """

        if type(self) is not type(other):
            return -1

        return cmp(self._ref, other._ref)

    def __hash__(self):
        """ Return a hash value for the object. """

        if self._cls is not None:
            hashable = (self._ref, self._fn)

        else:
            hashable = self._ref

        return hash(hashable)

#### EOF ######################################################################
