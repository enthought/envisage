""" An Egg based extension provider. """


# Standard library imports.
import logging, pkg_resources

# Enthought library imports.
from enthought.traits.api import Instance

# Local imports.
from extension_provider import ExtensionProvider


# Logging.
logger = logging.getLogger(__name__)


class EggExtensionProvider(ExtensionProvider):
    """ An Egg based extension provider. """

    #### 'EggExtensionProvider' interface #####################################

    # The working set that contains the eggs that contain the extensions that
    # live in the house that Jack built ;^) By default we use the global
    # working set.
    working_set = Instance(pkg_resources.WorkingSet, pkg_resources.working_set)

    ###########################################################################
    # 'IExtensionRegistry' interface.
    ###########################################################################

    def get_extensions(self, extension_point, load=True, lhs=False):
        """ Return all contributions to an extension point. """

        extensions = []
        for entry_point in self.working_set.iter_entry_points(extension_point):
            # fixme: Egg entry point syntax is somewhat limiting. Sometimes
            # it is useful to use the LHS of the entry point expression.
            if lhs:
                extension = entry_point.name

            else:
                if load:
                    extension = entry_point.load()

                else:
                    extension = entry_point.module_name

            extensions.append(extension)
            
        logger.debug('extensions to %s are %s', extension_point, extensions)

        return extensions

#### EOF ######################################################################
