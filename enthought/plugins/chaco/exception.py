""" Exception types. """

class ResourceAlreadyBoundError(Exception):
    """ Resource already bound.

    This exception is thrown when an attempt is made to bind a PlotDataFactory
    for a resource type that already has a PlotDataFactory bound.
    """

class ResourceNotFoundError(Exception):
    """ Resource not found.

    This exception is thrown when an attempt is made to access a PlotDataFactory
    for a resource which does not have a factory bound.
    """
