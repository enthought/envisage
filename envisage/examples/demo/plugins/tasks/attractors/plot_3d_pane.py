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
from attractors.model.i_model_3d import IModel3d
from mayavi.core.ui.mayavi_scene import MayaviScene

# Enthought library imports.
from mayavi.tools.mlab_scene_model import MlabSceneModel
from tvtk.pyface.scene_editor import SceneEditor

from pyface.tasks.api import TraitsTaskPane
from traits.api import Dict, Instance, List, on_trait_change, Str
from traitsui.api import EnumEditor, HGroup, Item, Label, View


class Plot3dPane(TraitsTaskPane):
    #### 'ITaskPane' interface ################################################

    id = "example.attractors.plot_3d_pane"
    name = "Plot 3D Pane"

    #### 'Plot3dPane' interface ###############################################

    active_model = Instance(IModel3d)
    models = List(IModel3d)

    scene = Instance(MlabSceneModel, ())

    view = View(
        HGroup(
            Label("Model: "),
            Item("active_model", editor=EnumEditor(name="_enum_map")),
            show_labels=False,
        ),
        Item(
            "scene",
            editor=SceneEditor(scene_class=MayaviScene),
            show_label=False,
        ),
        resizable=True,
    )

    #### Private traits #######################################################

    _enum_map = Dict(IModel3d, Str)

    ###########################################################################
    # Protected interface.
    ###########################################################################

    #### Trait change handlers ################################################

    @on_trait_change("active_model.points")
    def _update_scene(self):
        self.scene.mlab.clf()
        if self.active_model:
            x, y, z = self.active_model.points.swapaxes(0, 1)
            self.scene.mlab.plot3d(x, y, z, line_width=1.0, tube_radius=None)

    @on_trait_change("models[]")
    def _update_models(self):
        # Make sure that the active model is valid with the new model list.
        if self.active_model not in self.models:
            self.active_model = self.models[0] if self.models else None

        # Refresh the EnumEditor map.
        self._enum_map = dict((model, model.name) for model in self.models)
