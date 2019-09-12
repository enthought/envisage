# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" The traits UI handler for the text editor. """


# Enthought library imports.
from traitsui.api import Handler


class TextEditorHandler(Handler):
    """ The traits UI handler for the text editor. """

    ###########################################################################
    # 'TextEditorHandler' interface.
    ###########################################################################

    # fixme: We need to work out how to create these 'dispatch' methods
    # dynamically! Plugins will want to add bindings to the editor to bind
    # a key to an action.
    def run(self, info):
        """ Run the text as Python code. """

        info.object.run()

        return

    def save(self, info):
        """ Save the text to disk. """

        info.object.save()

        return

#### EOF ######################################################################
