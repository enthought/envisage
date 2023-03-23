# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

# Local imports.
from attractors.model.i_model_2d import IModel2d

# Enthought library imports.
from traits.api import Enum, Str


class IPlottable2d(IModel2d):
    plot_type = Enum("line", "scatter")

    x_label = Str()
    y_label = Str()
