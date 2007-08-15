""" A node in the preferences hierarchy. """


# Enthought library imports.
from enthought.traits.api import Any, Dict, HasTraits, Instance, Str
from enthought.traits.api import implements

# Local imports.
from i_preferences import IPreferences


class Preferences(HasTraits):
    """ A node in the preferences hierarchy. """

    implements(IPreferences)

    #### 'IPreferences' interface #############################################

    # The perent node (None if this is the root node).
    parent = Instance(IPreferences)

    # The name of the node (relative to the parent).
    name = Str('root')
    
    #### 'Preferences' interface ##############################################

    # The node's children.
    children = Dict(Str, IPreferences)

    # The node's actual preferences.
    preferences = Dict(Str, Any)
    
    ###########################################################################
    # 'IPreferences' interface.
    ###########################################################################

    def keys(self, path=''):
        """ Return the preference keys of the node at the specified path. """

        components = path.split('.')

        if len(components) == 1:
            keys = self.preferences.keys()

        else:
            node = self.node('.'.join(components))
            keys = node.keys()

        return keys
        
    def node(self, path):
        """ Return the node at the specified path.

        Create any intermediate nodes if they do not exist.

        """

        components = path.split('.')

        node = self
        for component in components:
            child = node.children.get(component)
            if child is None:
                child = type(node)(name=component, parent=node)
                node.children[component] = child

            node = child

        return node

    def get(self, key, default=None):
        """ Get the value of a preference. """

        components = key.split('.')

        if len(components) == 1:
            value = self.preferences.get(key, default)

        else:
            node  = self.node('.'.join(components[:-1]))
            value = node.get(components[-1], default)

        return value

    def set(self, key, value):
        """ Set the value of a preference. """

        components = key.split('.')

        if len(components) == 1:
            self.preferences[key] = value

        else:
            node  = self.node('.'.join(components[:-1]))
            node.set(components[-1], value)

        return

    def load(self, filename):
        """ Load the node contents from a 'ConfigObj' file. """

        from configobj import ConfigObj
        
        config_obj = ConfigObj(filename)

        for name, value in config_obj.items():
            if isinstance(value, dict):
                node = self.node(name)
                for k, v in value.items():
                    node.set(k, v)

            else:
                self.set(name, value)

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




