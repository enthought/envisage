""" An attempt at type-safe casting. """


# Enthought library imports.
from enthought.traits.api import Any, HasTraits, Interface


class ProtocolError(Exception):
    """ A protocol error. """

    
class TypeSafeAdapter(HasTraits):
    """ An attempt at type-safe casting. """

    # The object that we cast.
    adaptee  = Any

    # The protocol that we cast it to.
    protocol = Any

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, adaptee, protocol):
        """ Constructor. """

        super(HasTraits, self).__init__(adaptee=adaptee, protocol=protocol)

        return
    
    def __getattribute__(self, name):
        """ Get an attribute of an object. """

        # Make sure that the attribute is actually a part of the protocol.
        protocol = object.__getattribute__(self, 'protocol')

        import inspect
        for cls in inspect.getmro(protocol):
            if cls is Interface or cls is object:
                continue

            if name in cls.__dict__.keys():
                break

        else:
            raise ProtocolError(
                '%s protocol has no attribute %s' % (protocol.__name__, name)
            )
        
        # Get the attribute as normal.
        adaptee = object.__getattribute__(self, 'adaptee')

        return getattr(adaptee, name)


def cast(obj, protocol):
    """ Cast an object to a protocol. """

    return TypeSafeAdapter(obj, protocol)

#### EOF ######################################################################
