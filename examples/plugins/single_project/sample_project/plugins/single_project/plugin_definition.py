#-----------------------------------------------------------------------------
#
#  Copyright (c) 2007 by Enthought, Inc.
#  All rights reserved.
#
#-----------------------------------------------------------------------------

"""
The env application's extension of the single project plugin.

"""

# Standard imports
import os
import sys

# Enthought library imports.
from envisage.api import Plugin, ServiceOffer
from envisage.ui.single_project.api import FactoryDefinition
from traits.api import List

# This module's package.
PKG = '.'.join(__name__.split('.')[:-1])

# Globally unique identifier.
ID = 'plugins.single_project'

###############################################################################
# `EnvProjectPlugin` class.
###############################################################################
class EnvProjectPlugin(Plugin):

    # Extension point Ids.
    FACTORY_DEFINITIONS = 'envisage.ui.single_project.factory_definitions'

    # The plugin's name.
    name = 'Env Project Plugin'

    ###### Contributions to extension points made by this plugin ######

    # Factory definition we contribute to.
    factory_definitions = List(contributes_to=FACTORY_DEFINITIONS)

    # Private methods.
    def _factory_definitions_default(self):
        """ Trait initializer. """
        factory_definition = FactoryDefinition(
            class_name = '%s.env_project_factory.EnvProjectFactory' % ID,
            priority = 10,
        )
        return [factory_definition]

    # TODO: Add contributions project action set.
