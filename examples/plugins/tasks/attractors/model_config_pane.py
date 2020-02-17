# Enthought library imports.
from pyface.tasks.api import TraitsDockPane
from traits.api import HasTraits, Instance
from traitsui.api import Item, View


class ModelConfigPane(TraitsDockPane):
    """ A simple dock pane for editing an attractor model's configuration
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
