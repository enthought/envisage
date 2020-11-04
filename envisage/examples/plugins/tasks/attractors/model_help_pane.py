# Standard library imports.
import codecs
import os.path

# Enthought library imports.
from pyface.tasks.api import TraitsDockPane
from traits.api import HasTraits, Instance, Property, Str, cached_property
from traitsui.api import HTMLEditor, Item, View

# Constants.
HELP_PATH = os.path.join(os.path.dirname(__file__), "help")


class ModelHelpPane(TraitsDockPane):
    """ A dock pane for viewing any help associated with a model.
    """

    #### 'ITaskPane' interface ################################################

    id = "example.attractors.model_help_pane"
    name = "Model Information"

    #### 'ModelConfigPane' interface ##########################################

    model = Instance(HasTraits)

    html = Property(Str, depends_on="model")

    view = View(
        Item(
            "pane.html",
            editor=HTMLEditor(base_url=HELP_PATH, open_externally=True),
            show_label=False,
        ),
        width=300,
        resizable=True,
    )

    ###########################################################################
    # Protected interface.
    ###########################################################################

    @cached_property
    def _get_html(self):
        """ Fetch the help HTML for the current model.
        """
        if self.model is None:
            return "No model selected."

        # Determine the name of the model.
        model = self.model
        while hasattr(model, "adaptee"):
            model = model.adaptee
        name = model.__class__.__name__.lower()

        # Load HTML file, if possible.
        path = os.path.join(HELP_PATH, name + ".html")
        if os.path.isfile(path):
            with codecs.open(path, "r", "utf-8") as f:
                return f.read()
        else:
            return "No information available for model."
