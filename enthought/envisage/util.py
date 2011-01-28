""" Utility functions used internally by Envisage. """


def camel_case_to_words(s):
    """ Turn a string from CamelCase into words separated by spaces.

    e.g. 'CamelCase' -> 'Camel Case'

    """

    def add_space_between_words(s, c):
        # We detect a word boundary if the character we are looking at is
        # upper case, but the character preceding it is lower case.
        if len(s) > 0 and s[-1].islower() and c.isupper():
            return s + ' ' + c

        return s + c

    return reduce(add_space_between_words, s, '')

#### EOF ######################################################################
