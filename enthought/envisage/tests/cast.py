""" An attempt at type-safe casting. """


# Standard library imports.
import inspect

# Enthought library imports.
from enthought.traits.api import Any, HasTraits, Interface


class ProtocolError(Exception):
    """ A protocol error. """


def cast(adaptee, protocol):
    """ Cast an object to a protocol in type-safe manner! """

    class TypeSafeAdapter(adaptee.__class__):
        """ An attempt at type-safe casting. """

        # The object that we are adapiting.
        tsa_adaptee = Any

        # The protocol that we are adapting it to.
        tsa_protocol = Any

        #######################################################################
        # 'object' interface.
        #######################################################################

        def __getattribute__(self, name):
            """ Get an attribute of an object. """

            adaptee = object.__getattribute__(self, 'tsa_adaptee')

            # Ignore any calls internal to the object.
            caller = inspect.currentframe().f_back
            if 'self' in caller.f_locals and caller.f_locals['self'] is self:
                return getattr(adaptee, name)
            
            # Make sure that the attribute is actually a part of the protocol.
            protocol = object.__getattribute__(self, 'tsa_protocol')

            for cls in inspect.getmro(protocol):
                if cls is object:
                    continue

                # fixme: Our type-hierarechy is kinda screwy! We need this to
                # allow the adapters to be able to access 'HasTraits'
                # attributes and methods like 'on_trait_change', but of course
                # there is no interface that these methods are on.
                if cls is Interface:
                    cls = HasTraits

                if name in cls.__dict__.keys():
                    break
                
            else:
                raise ProtocolError(
                    '%s protocol has no attribute %s' % (
                        protocol.__name__, name
                    )
                )

            # Get the attribute as normal.
            return getattr(adaptee, name)

    return TypeSafeAdapter(tsa_adaptee=adaptee, tsa_protocol=protocol)

#### EOF ######################################################################
