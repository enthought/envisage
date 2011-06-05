#-----------------------------------------------------------------------------
#
#  Copyright (c) 2007 by Enthought, Inc.
#  All rights reserved.
#
#-----------------------------------------------------------------------------

# Enthought library imports.
from chaco.chaco_plot_editor import ChacoPlotItem
from blockcanvas.numerical_modeling.numeric_context.api import NumericContext
from traits.api import adapts, Array, Enum, Float, HasTraits, \
    Instance, Range, Property
from traitsui.api import Group, Item, RangeEditor, ITreeNode, \
    ITreeNodeAdapter, View
from numpy import arange


class DataView(HasTraits):
    volume = Array
    pressure = Property(Array, depends_on=['temperature','attraction','totVolume'])
    attraction = Range(low=-50.0,high=50.0,value=0.0)
    totVolume = Range(low=.01,high=100.0,value=0.01)
    temperature = Range(low=-50.0,high=50.0,value=50.0)
    r_constant= Float(8.314472)
    plot_type = Enum("line", "scatter")

    data_view = View(ChacoPlotItem("volume", "pressure",
                               type_trait="plot_type",
                               resizable=True,
                               x_label="Volume",
                               y_label="Pressure",
                               x_bounds=(-10,120),
                               x_auto=False,
                               y_bounds=(-2000,4000),
                               y_auto=False,
                               color="blue",
                               bgcolor="white",
                               border_visible=True,
                               border_width=1,
                               title='Pressure vs. Volume',
                               padding_bg_color="lightgray"),
                       Item(name='attraction'),
                       Item(name='totVolume'),
                       Item(name='temperature'),
                       Item(name='r_constant',style='readonly'),
                       Item(name='plot_type'),
                       resizable = True,
                       buttons = ["OK"],
                       title='Van der waal Equation',
                       width=900, height=500)

    def _volume_default(self):
      return arange(.1, 100)

    # Pressure is calculated whenever one of the elements the property depends on changes.
    def _get_pressure(self):
      return ((self.r_constant*self.temperature)/(self.volume - self.totVolume)) - (self.attraction/(self.volume*self.volume))




class Data(NumericContext):
    name = Property(depends_on = ['context_name'])
    # data_parameters = Property
    data_parameters = Instance(DataView)

    ###################################################################################
    # Object Methods
    ###################################################################################
    """ Contains all of the data for a data """
    def __init__(self, name="Unknown", **traits):
        super( Data, self ).__init__( **traits )
        self.context_name = name
        self.data_parameters = DataView()
        # self.data_parameters = DataView()
        # self['data_parameters'] = DataParameters(self)
        # TODO cgalvan: Init other data


    def __getstate__(self):
        """ Return the state of this object for pickling.

            Extended to remove transient traits, and also store version
            information.

        """

        # Obtain state from base class(es)
        state =  super(Data, self).__getstate__()

        # Add in our current version number.  Note use a different attribute
        # name from any base or derived class so that our numbers don't
        # override theirs.
        state['_data_version'] = 1

        return state


    def __setstate__(self, state):
        """ Restore the state of this object during unpickling.

            Extended to handle version upgrades.

        """

        # Get the version info out of the state dictionary.
        version = state.pop('_data_version', 0)

        # Upgrade to version 1.
        if version < 1:
            # Include dynamic bindings to all the numeric contexts in the
            # dictionary
            items_dict = {}

            if state.has_key('context_data'):
                context_data = state['context_data']
                if isinstance(context_data, dict) and len(context_data) > 0:
                    items_dict = context_data._dict

            if len(items_dict) > 0:
                self._add_all_items_as_dynamic_bindings_to_state(state,
                                                                 items_dict)

        # Restore the base class's state.
        super(Data, self).__setstate__(state)

        return


    ############################################################################
    # Protected Methods
    ############################################################################

#    def _get_data_parameters(self):
#        return self['data_parameters']

    def _get_data_parameters(self):
        return self.data_parameters

    def _get_name(self):
        return self.context_name


    def _set_name(self, new_name):
        self.context_name = new_name
        return


class DataAdapter(ITreeNodeAdapter):
    """ ITreeNodeAdapter for our custom Data object. """

    adapts(Data, ITreeNode)

    #-- ITreeNodeAdapter Method Overrides --------------------------------------

    def allows_children(self):
        """ Returns whether this object can have children.
        """
        return False

    def get_label(self):
        """ Gets the label to display for a specified object.
        """
        return self.adaptee.name

    def confirm_delete(self):
        """ Checks whether a specified object can be deleted.

        Returns
        -------
        * **True** if the object should be deleted with no further prompting.
        * **False** if the object should not be deleted.
        * Anything else: Caller should take its default action (which might
          include prompting the user to confirm deletion).
        """
        return None

    def when_label_changed(self, listener, remove):
        """ Sets up or removes a listener for the label being changed on a
            specified object.
        """
        self.adaptee.on_trait_change(listener, 'list_items',
            remove=remove, dispatch='ui')

    def get_tooltip(self):
        """ Gets the tooltip to display for a specified object.
        """
        return "Data"

    def get_icon(self, is_expanded):
        """ Returns the icon for a specified object.
        """
        return '<item>'

    def can_auto_close(self):
        """ Returns whether the object's children should be automatically
            closed.
        """
        return True

    def can_rename_me(self):
        """ Returns whether the object can be renamed.
        """
        return True

    def can_delete_me(self):
        """ Returns whether the object can be deleted.
        """
        return True





