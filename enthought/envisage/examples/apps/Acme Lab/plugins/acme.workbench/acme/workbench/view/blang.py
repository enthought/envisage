""" Used in the example to provide a Traits UI view via a UOL. """


# Enthought library imports.
from enthought.traits.api import HasTraits, Int, Str


class Blang(HasTraits):
    """ Used in the example to provide a Traits UI view via a UOL. """

    name = Str('A Blang')
    x    = Int(42)
    y    = Int(100)


# This is the symbol that the UOL references.
blang = Blang()

#### EOF ######################################################################
