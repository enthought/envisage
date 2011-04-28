""" The exception raised when trying to open a non-existent resource. """


class NoSuchResourceError(Exception):
    """ The exception raised when trying to open a non-existent resource. """

    def __init__(self, message=''):
        """ Constructor. """

        Exception.__init__(self, message)

        return

#### EOF ######################################################################
