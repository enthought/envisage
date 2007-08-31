""" A decorator for marking methods as extension contributors. """


def extension(id):
    """ A factory for extension decorators! """

    def decorator(fn):
        """ A decorator for marking methods as extension contributors. """

        fn.__extension_point__ = id

        return fn

    return decorator

#### EOF ######################################################################
