""" A view containing a yellow panel! """


# Local imports.
from color_view import ColorView


class YellowView(ColorView):
    """ A view containing a yellow panel! """

    #### 'IView' interface ####################################################

    # The view's name.
    name = 'Yellow'

    # The default position of the view relative to the item specified in the
    # 'relative_to' trait.
    position = 'bottom'

#### EOF ######################################################################
