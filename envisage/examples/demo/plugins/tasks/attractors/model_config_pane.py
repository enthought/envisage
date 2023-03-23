# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

# Enthought library imports.
from pyface.tasks.api import TraitsDockPane
from traits.api import HasTraits, Instance
from traitsui.api import Item, View


class ModelConfigPane(TraitsDockPane):
    """A simple dock pane for editing an attractor model's configuration
    options.
    """

    #### 'ITaskPane' interface ################################################

    id = "example.attractors.model_config_pane"
    name = "Model Configuration"

    #### 'ModelConfigPane' interface ##########################################

    model = Instance(HasTraits)

    view = View(
        Item("pane.model", style="custom", show_label=False), resizable=True
    )
