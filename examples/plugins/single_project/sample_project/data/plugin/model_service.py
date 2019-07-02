#-----------------------------------------------------------------------------
#
#  Copyright (c) 2007 by Enthought, Inc.
#  All rights reserved.
#
#-----------------------------------------------------------------------------

"""
The model service for the Data plugin.

"""

# Standard library imports.
import logging
import numpy

# Enthought library imports.
from envisage.api import ApplicationObject
from apptools.naming.unique_name import make_unique_name
from blockcanvas.numerical_modeling.numeric_context.api import NumericContext
from blockcanvas.numerical_modeling.units.unit_array import UnitArray
from scimath.units.api import convert,unit_manager
from scimath.units.mass import gram
from scimath.units.volume import cc
from scimath.units.length import meter
from scimath.units.geo_units import ppg, psi
from pyface.wx.clipboard import clipboard

# Data library imports.


# Setup a logger for this module
logger = logging.getLogger(__name__)


class ModelService(ApplicationObject):
    """
    The model service for the Dataplugin.

    """


    ##########################################################################
    # 'ModelService' interface
    ##########################################################################

    #### public methods ######################################################

    def delete_context_item(self, context, item_name):
        """ Deleting an item from a numeric context

        Parameters
        ----------
        context : NumericContext
        item_name : Str

        """

        if isinstance(context, NumericContext) and context.has_key(item_name):
            context.pop(item_name)
        else:
            logger.error('Invalid context or data not found in context')

        return
#### EOF #####################################################################
