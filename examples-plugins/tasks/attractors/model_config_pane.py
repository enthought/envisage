# Enthought library imports.
from enthought.pyface.tasks.api import TraitsDockPane
from enthought.traits.api import HasTraits, Instance
from enthought.traits.ui.api import Item, View


class ModelConfigPane(TraitsDockPane):
    """ A simple dock pane for editing an attractor model's configuration
        options.
    """

    #### 'ITaskPane' interface ################################################

    id = 'example.attractors.model_config_pane'
    name = 'Model Configuration'

    #### 'ModelConfigPane' interface ##########################################

    model = Instance(HasTraits)

    view = View(Item('model',
                     style = 'custom',
                     show_label = False),
                resizable = True)
