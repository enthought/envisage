# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" A definition of a category to be added to a class. """


# Enthought library imports.
from traits.api import HasTraits, Str


class Category(HasTraits):
    """ A definition of a category to be added to a class. """

    #### 'Category' interface #################################################

    # The name of the category class (the class that you want to add).
    class_name = Str

    # The name of the class that you want to add the category to.
    target_class_name = Str

#### EOF ######################################################################
