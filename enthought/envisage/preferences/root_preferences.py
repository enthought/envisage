""" The root preferences node. """


# Enthought library imports.
from enthought.traits.api import on_trait_change

# Local imports.
from preferences import Preferences


class RootPreferences(Preferences):
    """ The root preferences node.

    The root preferences node only contains child nodes - not actual
    preferences. Each child node represents a single preference *scope*.

    """
    
    ###########################################################################
    # 'IPreferences' interface.
    ###########################################################################
    
    def node(self, path):
        """ Return the node at the specified path.

        Create any intermediate nodes if they do not exist.

        """

        if len(path) == 0:
            raise ValueError('empty path')

        # The scope is up to the first '/'. The scope context (if any) is from
        # the first '/' to the last '/', and the actual preference path is the
        # rest!
        #
        # e.g. A preference path might look like this:-
        #
        # 'project/My Project/my.plugin.id/acme.ui.bgcolor'
        #
        # The scope is          'project'.
        # The scope context is  'My Project/my.plugin.id'
        # The preference key is 'acme.ui.bgcolor' 
        components = path.split('/')

        # Lookup the preference node that represents the scope.
        node = self._node(components[0])

        # If there was anything else in the path then pass it onto the scope.
        if len(components) > 1:
            node = node.node('/'.join(components[1:]))

        return node

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

#### EOF ######################################################################




