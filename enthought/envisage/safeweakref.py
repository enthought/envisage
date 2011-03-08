""" An implementation of weak references that works for bound methods.

This code is based on the code in the Python Cookbook, but you can call `ref`
for objects that are *not* bound methods too, in which case it just returns a
standard `weakref.ref`.

Weak references to bound methods are cached so that `ref(x) is ref(x)` as for
standard weakrefs, and the `ref` class defined here is therefore intended to be
used as a drop-in replacement for 'weakref.ref'.

"""


# Standard library imports.
import new, weakref


class ref(object):
    """ An implementation of weak references that works for bound methods. """

    # A cache containing the weak references we have already created.
    #
    # We cache the weak references by the object containing the associated
    # bound methods, hence this is a dictionary of dictionaries in the form:-
    #
    # { bound_method.im_self : { bound_method.im_func : ref } }
    #
    # This makes sure that when the object is garbage collected, any cached
    # weak references are garbage collected too.
    _cache = weakref.WeakKeyDictionary()
    
    def __new__(cls, obj, *args, **kw):
        """ Create a new instance of the class. """

        # If the object is a bound method then either get from the cache, or
        # create an instance of *this* class to behave like a regular weakref.
        if hasattr(obj, 'im_self'):
            func_cache = ref._cache.setdefault(obj.im_self, {})
            
            # If we haven't created a weakref to this bound method before, then
            # create one and cache it.
            instance = func_cache.get(obj.im_func)
            if instance is None:
                instance = object.__new__(cls, obj, *args, **kw)
                func_cache[obj.im_func] = instance
                
        # Otherwise, just return a regular weakref (because we aren't
        # returning an instance of *this* class our constructor does not get
        # called).
        else:
            instance = weakref.ref(obj)

        return instance
        
    def __init__(self, obj):
        """ Create a weak reference to a bound method object.

        'obj' is *always* a bound method because in the '__new__' method we
        don't return an instance of this class if it is not, and hence this
        constructor doesn't get called.

        """

        self._cls = obj.im_class
        self._fn  = obj.im_func
        self._ref = weakref.ref(obj.im_self)
            
        return

    def __call__(self):
        """ Return a strong reference to the object.

        Return None if the object has been garbage collected.

        """

        obj = self._ref()
        if obj is not None:
            obj = new.instancemethod(self._fn, obj, self._cls)

        return obj

#### EOF ######################################################################
