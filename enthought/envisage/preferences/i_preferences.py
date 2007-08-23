""" The interface for a node in a preference hierarchy. """


# Enthought library imports.
from enthought.traits.api import Instance, Interface, Str


class IPreferences(Interface):
    """ The interface for a node in a preference hierarchy. """

    # The absolute path to this node from the root node (the empty string if
    # this node *is* the root node).
    path = Str
    
    # The parent node (None if this node *is* the root node).
    parent = Instance('IPreferences')

    # The name of the node relative to the parent (the empty string if this
    # node *is* the root node).
    name = Str

    def get(self, path, default=None):
        """ Get the value of the preference at the specified path.

        If no value exists for the path (or any part of the path does not
        exist) then return the default value.

        Preference values are *always* returned as strings.
        
        Raise a 'ValueError' exception if the path is the empty string.

        e.g::

          bgcolor = preferences.get('acme.ui.bgcolor', 'blue')

        """

    def keys(self, path=''):
        """ Return the preference keys of the node at the specified path.

        If the path is empty then return the preference keys of *this* node.
        
        """
        
    def node(self, path):
        """ Return the node at the specified path.

        Raise a 'ValueError' exception if the path is the empty string.

        Any missing nodes are created automatically.

        e.g::

          node = preferences.node('acme.ui')
          bgcolor = node.get('bgcolor')
          
        """
        
    def set(self, path, value):
        """ Set the value of the preference at the specified path.

        Raise a 'ValueError' exception if the path is the empty string.
        
        Any missing nodes are created automatically.

        e.g::

            preferences.set('acme.ui.bgcolor', 'blue')

        """

#### EOF ######################################################################
