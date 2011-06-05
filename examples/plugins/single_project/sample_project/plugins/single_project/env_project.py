#-----------------------------------------------------------------------------
#
#  Copyright (c) 2007 by Enthought, Inc.
#  All rights reserved.
#
#-----------------------------------------------------------------------------

"""

Test envisage project.

"""

# System library imports.
import logging

# Enthought library imports.
from envisage.ui.single_project.api import Project
from apptools.naming.unique_name import make_unique_name
from blockcanvas.numerical_modeling.numeric_context.numeric_context import \
    NumericContext
from traits.api import adapts, property_depends_on, Property, List
from traitsui.api import Group, ITreeNode, ITreeNodeAdapter, View
from traitsui.menu import Action, Menu

# Data import
from data.data import Data

# Setup a logger for this module
logger = logging.getLogger(__name__)


class EnvProject(Project, NumericContext):
    """
    Envisage project.

    """

    ##########################################################################
    # Attributes
    ##########################################################################

    #### public 'Project' interface ##########################################

    # The location of this project on the filesystem.  The default value
    # depends on the runtime environment so we use a traits default method to
    # set it.
    #
    # Overridden here to a File to use the File dialog since we're saving
    # projects as files.


    # Set up the naming environment.
#    klass_name = "apptools.naming.InitialContextFactory"
#    environment = {Context.INITIAL_CONTEXT_FACTORY : klass_name}
#
#    # Create an initial context.
#    context = InitialContext(environment)

    # The list of names bound in this context:
    list_names = Property(List)

    # The list of items bound in this context:
    list_items = Property(List)

    # The UI view to use when creating a new project
    traits_view = View(
        Group('location'),
        title = 'New Env Project',
        id = 'plugins.single_project.env_project.EnvProject',
        buttons = [ 'OK', 'Cancel' ],

        # Ensure closing via the dialog close button is the same
        # as clicking cancel.
        close_result = False,

        # Ensure the user can resize the dialog.
        resizable = True,
        )


    ##########################################################################
    # 'object' interface
    ##########################################################################

    #### operator methods ####################################################

    def __getstate__(self):
        """ Return the state of this object for pickling.

            Extended to remove transient traits, and also store version
            information.

        """

        # Obtain state from base class(es)
        state =  super(EnvProject, self).__getstate__()

        # Add in our current version number.  Note use a different attribute
        # name from any base or derived class so that our numbers don't
        # override theirs.
        state['_env_project_version'] = 1

        return state


    def __setstate__(self, state):
        """ Restore the state of this object during unpickling.

            Extended to handle version upgrades.

        """

        # Get the version info out of the state dictionary.
        version = state.pop('_env_project_version', 0)

        # Upgrade to version 1.
        if version < 1:
            # Include dynamic bindings to all the numeric contexts in the
            # dictionary
            items_dict = {}

            if state.has_key('context_data'):
                context_data = state['context_data']
                if isinstance(context_data, dict) and len(context_data) > 0:
                    items_dict = state['context_data']._dict

            if len(items_dict) > 0:
                self._add_all_items_as_dynamic_bindings_to_state(state,
                                                                 items_dict)


        # Restore the base class's state.
        super(EnvProject, self).__setstate__(state)

        return


    ##########################################################################
    # 'EnvProject' interface
    ##########################################################################

    #### property implementaions #############################################

    @property_depends_on('dict_modified')
    def _get_list_names(self):
        """
        List the names bound in this context.

        """

        result = [k for k, v in self.items() if isinstance(v, Data)]
        result.sort()
        return result

    @property_depends_on('dict_modified')
    def _get_list_items(self):
        """
        List the items bound in this context.

        """
        result = self.items()
        result.sort(lambda l, r: cmp(l[0], r[0]))
        return [v for n, v in result]

    def create_data(self, name='Data'):
        """
        Create a new data within this project.

        The new data is initialized with the specified trait values and is
        automatically added to this project.

        """

        # Ensure the name we associate with the data within this project is
        # unique.
        name = make_unique_name(name, self.keys())

        # Create the new data
        data = Data(name)

        # Add it to ourself.
        self.bind_dynamic(data, 'context_name')

        logger.debug('Added new data (%s) to EnvProject (%s) with '
            'name (%s)', data, self, name)

        return data


class EnvProjectAdapter(ITreeNodeAdapter):
    """ EnvProjectAdapter for our custom project. """

    adapts(EnvProject, ITreeNode)

    #-- ITreeNodeAdapter Method Overrides --------------------------------------

    def allows_children(self):
        """ Returns whether this object can have children.
        """
        return True

    def has_children(self):
        """ Returns whether the object has children.
        """
        return (len(self.adaptee.list_items) > 0)

    def get_children(self):
        """ Gets the object's children.
        """
        return self.adaptee.list_items

    def get_children_id(self):
        """ Gets the object's children identifier.
        """
        return 'list_items'

    def append_child(self, child=None):
        """ Appends a child to the object's children.
        """
        data = self.adaptee.create_data()

    def confirm_delete(self):
        """ Checks whether a specified object can be deleted.

        Returns
        -------
        * **True** if the object should be deleted with no further prompting.
        * **False** if the object should not be deleted.
        * Anything else: Caller should take its default action (which might
          include prompting the user to confirm deletion).
        """
        return False

    def delete_child(self, index):
        """ Deletes a child at a specified index from the object's children.
        """
        # Remove the child at the specified index.
        child = self.adaptee.list_items[index]
        self.adaptee._unbind_dynamic(child, 'context_name')

    def when_children_replaced(self, listener, remove):
        """ Sets up or removes a listener for children being replaced on a
            specified object.
        """
        self.adaptee.on_trait_change(listener, 'list_items',
                              remove=remove, dispatch='ui')

    def get_label(self):
        """ Gets the label to display for a specified object.
        """
        return self.adaptee.name

    def get_menu(self):
        """ Returns the right-click context menu for an object.
        """
        return Menu(*[
            Action(name='Create Data',
                action='node.adapter.append_child',
            )]
        )

    def get_tooltip(self):
        """ Gets the tooltip to display for a specified object.
        """
        return "Project"

    def get_icon(self, is_expanded):
        """ Returns the icon for a specified object.
        """
        return '<open>'

    def can_rename(self):
        """ Returns whether the object's children can be renamed.
        """
        return True

    def can_copy(self):
        """ Returns whether the object's children can be copied.
        """
        return True

    def can_delete(self):
        """ Returns whether the object's children can be deleted.
        """
        return True

    def can_auto_open(self):
        """ Returns whether the object's children should be automatically
            opened.
        """
        return True

    def can_auto_close(self):
        """ Returns whether the object's children should be automatically
            closed.
        """
        return False

### EOF ######################################################################

