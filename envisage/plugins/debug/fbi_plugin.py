#-------------------------------------------------------------------------------
#
#  wxPython Test Plugin.
#
#  Written by: David C. Morrill
#
#  Date: 10/18/2005
#
#  (c) Copyright 2005 by Enthought, Inc.
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

import sys

from traits.api import push_exception_handler

from envisage.api import Plugin

from etsdevtools.debug.fbi import enable_fbi, fbi

#-------------------------------------------------------------------------------
#  'FBIPlugin' class:
#-------------------------------------------------------------------------------

class FBIPlugin ( Plugin ):
    """ FBIPython plugin. """

    #---------------------------------------------------------------------------
    #  'Plugin' interface:
    #---------------------------------------------------------------------------

    def start ( self, application ):
        """ Starts the plugin.
        """
        # Tell the FBI to wiretap all unauthorized exceptions:
        enable_fbi()
        push_exception_handler( handler = lambda obj, name, old, new: fbi(),
                                locked  = False,
                                main    = True )

    def stop ( self, application ):
        """ Stops the plugin.
        """
        pass

