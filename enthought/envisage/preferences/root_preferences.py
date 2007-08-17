""" The root preferences node. """


# Major package imports.
from configobj import ConfigObj

# Enthought library imports.
from enthought.traits.api import Any, Dict, HasTraits, Instance, Property, Str
from enthought.traits.api import implements, on_trait_change

# Local imports.
from preferences import Preferences


class RootPreferences(Preferences):
    """ The root preferences node. """
    
    ###########################################################################
    # 'IPreferences' interface.
    ###########################################################################
    
    def keys(self, path=''):
        """ Return the preference keys of the node at the specified path. """

        raise NotImplementedError
        
    def node(self, path):
        """ Return the node at the specified path.

        Create any intermediate nodes if they do not exist.

        """

        if len(path) == 0:
            raise ValueError('empty path')

        # The scope is up to the first '/'. The scope context (if any) is up to
        # between the first '/' and last '/', the actual preference path is the
        # rest.
        components = path.split('/')

        # If there is only one component then it is the scope name, so the
        # child is in this node.
        node = self._node(components[0])
        if len(components) > 1:
            node = node.node('.'.join(components[1:]))

        return node

    def get(self, path, default=None):
        """ Get the value of a preference at the specified path. """

        raise NotImplementedError

    def set(self, path, value):
        """ Set the value of a preference at the specified path. """

        raise NotImplementedError

    ###########################################################################
    # 'RootPreferences' interface.
    ###########################################################################

    @on_trait_change('children')
    @on_trait_change('children_items')
    def _when_children_changed(self, obj, trait_name, old, new):
        """ Trait change handler. """

        for child in self.children:
            child.parent = self

        return
        
    ###########################################################################
    # Protected 'Preferences' interface.
    ###########################################################################

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




