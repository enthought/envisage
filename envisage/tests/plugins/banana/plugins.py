""" Plugin finder for the current package. """


def get_plugins():
    """ Get the plugins from this package. """

    from .banana_plugin import BananaPlugin

    return [BananaPlugin()]

#### EOF #######################################################################
