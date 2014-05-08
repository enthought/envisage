""" Plugin finder for the current package. """


def get_plugins():
    """ Get the plugins from this package. """

    from .orange_plugin import OrangePlugin

    return [OrangePlugin()]

#### EOF #######################################################################
