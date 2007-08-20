""" A node in a preferences hierarchy. """


# Standard library imports.
import logging

# Enthought library imports.
from enthought.traits.api import Any, Dict, HasTraits, Instance, Property, Str
from enthought.traits.api import implements

# Local imports.
from i_preferences import IPreferences


# Logging.
logger = logging.getLogger(__name__)


class Preferences(HasTraits):
    """ A node in a preferences hierarchy. """

    implements(IPreferences)

    #### 'IPreferences' interface #############################################

    # The absolute path to this node from the root node (the empty string if
    # this node *is* the root node).
    path = Property(Str)
    
    # The parent node (None if this node *is* the root node).
    parent = Instance(IPreferences)

    # The name of the node relative to the parent (the empty string if this
    # node *is* the root node).
    name = Str
    
    #### 'Preferences' interface ##############################################

    # The node's children.
    children = Dict(Str, IPreferences)
    
    # The node's actual preferences.
    preferences = Dict(Str, Any)
    
    ###########################################################################
    # 'IPreferences' interface.
    ###########################################################################

    #### Trait properties #####################################################
    
    def _get_path(self):
        """ Property getter. """

        names = []

        node = self
        while node.parent is not None:
            names.append(node.name)
            node = node.parent

        names.reverse()
        
        return '.'.join(names)
    
    #### Methods ##############################################################

    def get(self, path, default=None):
        """ Get the value of a preference at the specified path. """

        if len(path) == 0:
            raise ValueError('empty path')

        components = path.split('.')

        if len(components) == 1:
            value = self._get(path, default)

        else:
            node = self
            for key in components[:-1]:
                node = node.children.get(key)
                if node is None:
                    value = default
                    break

            else:
                value = node.get(components[-1])

        return value

    def keys(self, path=''):
        """ Return the preference keys of the node at the specified path. """

        if len(path) == 0:
            keys = self._keys()

        else:
            node = self.node(path)
            keys = node.keys()

        return keys

    def node(self, path):
        """ Return the node at the specified path.

        Create any intermediate nodes if they do not exist.

        """

        if len(path) == 0:
            raise ValueError('empty path')
        
        components = path.split('.')

        node = self._node(components[0])
        if len(components) > 1:
            node = node.node('.'.join(components[1:]))

        return node

    def has_child(self, name):
        """ Return True if the node has a child with the specified name. """

        return self.children.has_key(name)
    
    def set(self, path, value):
        """ Set the value of a preference at the specified path. """

        if len(path) == 0:
            raise ValueError('empty path')

        components = path.split('.')

        if len(components) == 1:
            self._set(path, value)

        else:
            node = self.node('.'.join(components[:-1]))
            node.set(components[-1], value)

        return

    ###########################################################################
    # 'Preferences' interface.
    ###########################################################################

    def load(self, file_or_filename):
        """ Load a 'ConfigObj' file into the node.

        This is a *merge* operation i.e. the contents of the file are added to
        the node.

        """

        logger.debug('loading preferences from %s', file_or_filename)

        # Do the import here so that we don't make 'ConfigObj' a requirement
        # if preferences aren't used.
        from configobj import ConfigObj

        config_obj = ConfigObj(file_or_filename)
        for name, value in config_obj.items():
            self._add_dictionary_to_node(self.node(name), value)

        return

    def save(self, filename=None):
        """ Save the node to a 'ConfigObj' file. """

        # Do the import here so that we don't make 'ConfigObj' a requirement
        # if preferences aren't used.
        from configobj import ConfigObj
        
        logger.debug('saving preferences to %s', filename)

        config_obj = ConfigObj(filename)
        self._save(self, config_obj)
        config_obj.write()
        
        return

    ###########################################################################
    # Protected 'Preferences' interface.
    ###########################################################################

    def _get(self, key, default=None):
        """ Get the value of a preference in this node. """

        return self.preferences.get(key, default)

    def _set(self, key, value):
        """ Set the value of a preference in this node. """

        self.preferences[key] = value

        return

    def _keys(self):
        """ Return the preference keys of *this* node. """

        return self.preferences.keys()

    def _node(self, name):
        """ Return the child node with the specified name.

        Create the child node if it does not exist.

        """
            
        node = self.children.get(name)
        if node is None:
            node = self._create_child(name)

        return node

    def _create_child(self, name):
        """ Create a child node with the specified name. """

        child = type(self)(name=name, parent=self)
        self.children[name] = child

        return child

    def _save(self, node, config_obj):
        """ Save a node to a 'ConfigObj' object. """

        if len(node.preferences) > 0:
            config_obj[node.path] = node.preferences.copy()

        for child in node.children.values():
            self._save(child, config_obj)

        return
        
    ###########################################################################
    # Private interface.
    ###########################################################################

    def _add_dictionary_to_node(self, node, dictionary):
        """ Add the contents of a dictionary to a node's preferences. """

        for name, value in dictionary.items():
            node.set(name, value)

        return
    
    ###########################################################################
    # Debugging interface.
    ###########################################################################

    def dump(self, indent=''):
        """ Dump the preferences hierarchy to stdout. """

        if indent == '':
            print
            
        print indent, 'Node(%s)' % self.name, self.preferences
        indent += '  '

        for child in self.children.values():
            child.dump(indent)
        
        return
    
#### EOF ######################################################################




