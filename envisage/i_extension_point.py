""" The interface for extension points. """


# Enthought library imports.
from traits.api import Instance, Interface, Str, TraitType


class IExtensionPoint(Interface):
    """ The interface for extension points. """

    # A description of what the extension point is and does! (it is called
    # the slightly dubious, 'desc', instead of 'description', or, to be more
    # 'Pythonic', maybe 'doc' to match the 'desc' metadata used in traits).
    desc = Str

    # The extension point's unique identifier.
    #
    # Where 'unique' technically means 'unique within the extension registry',
    # but since the chances are that you will want to include extension points
    # from external sources, this really means 'globally unique'! Using the
    # Python package path might be useful here ;^)
    #
    # e.g. 'envisage.ui.workbench.views'
    id = Str

    # A trait type that describes what can be contributed to the extension
    # point.
    #
    # e.g. List(Str)
    trait_type = Instance(TraitType)

#### EOF ######################################################################
