# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

""" This code has been inspired from the IPython repository

https://github.com/ipython/ipython/blob/2.x/examples/Embedding/internal_ipkernel.py

"""
from __future__ import absolute_import, print_function, unicode_literals

import atexit
import warnings

import ipykernel.connect
import six

from envisage.plugins.ipython_kernel.kernelapp import IPKernelApp
from traits.api import Any, HasStrictTraits, Instance, List


# Allow unregistration of atexit handlers registered by IPython machinery.

if six.PY2:
    def atexit_unregister(func):
        # Replace the contents, not the list itself, in case anyone else
        # is keeping references to it. Also use 'not thing == func' instead
        # of 'thing != func' to match the semantics of the Python 3 code.
        atexit._exithandlers[:] = list(
            handler for handler in atexit._exithandlers
            if not handler[0] == func
        )
else:
    from atexit import unregister as atexit_unregister


def _gui_kernel(gui_backend):
    """ Launch and return an IPython kernel GUI with support.

    Parameters
    ----------
    gui_backend -- string or None
      The GUI mode used to initialize the GUI mode. For options, see
      the `ipython --gui` help pages. If None, the kernel is initialized
      without GUI support.
    """

    kernel = IPKernelApp.instance()

    argv = ['python']
    if gui_backend is not None:
        argv.append('--gui={}'.format(gui_backend))
    kernel.initialize(argv)

    return kernel


class InternalIPKernel(HasStrictTraits):
    """ Represents an IPython kernel and the consoles attached to it.
    """

    #: The IPython kernel.
    ipkernel = Instance(IPKernelApp)

    #: A list of connected Qt consoles.
    consoles = List()

    #: The kernel namespace.
    #: Use `Any` instead of `Dict` because this is an IPython dictionary
    #: object.
    namespace = Any()

    #: The values used to initialize the kernel namespace.
    #: This is a list of tuples (name, value).
    initial_namespace = List()

    def init_ipkernel(self, gui_backend=None):
        """ Initialize the IPython kernel.

        Parameters
        ----------
        gui_backend -- string, optional
            The GUI mode used to initialize the GUI event loop integration. For
            options, see the `ipython --gui` help pages. If not given, no event
            loop integration is set up.

        .. note:: Use of this argument is deprecated!
        """
        # For backwards compatibility, we allow a kernel to be initialized
        # twice, and we ignore the second initialization, but warn.
        if self.ipkernel is not None:
            warnings.warn(
                (
                    "The IPython kernel has already been initialized. A "
                    "second call to init_ipkernel has no effect. In the "
                    "future, a second initialization may become an error."
                ),
                DeprecationWarning,
            )
            return

        if gui_backend is not None:
            warnings.warn(
                (
                    "The gui_backend argument is deprecated. "
                    "Integration with a GUI event loop can be "
                    "achieved by setting the 'eventloop' attribute on the "
                    "kernel instance"
                ),
                DeprecationWarning,
            )

        # Start IPython kernel with GUI event loop support
        self.ipkernel = _gui_kernel(gui_backend)

        # This application will also act on the shell user namespace
        self.namespace = self.ipkernel.shell.user_ns
        self.namespace.update(dict(self.initial_namespace))

    def new_qt_console(self):
        """ Start a new qtconsole connected to our kernel. """
        console = ipykernel.connect.connect_qtconsole(
            self.ipkernel.connection_file,
            argv=['--no-confirm-exit'],
        )
        self.consoles.append(console)
        return console

    def cleanup_consoles(self):
        """ Kill all existing consoles. """
        for c in self.consoles:
            c.kill()
            c.wait()
            c.stdout.close()
            c.stderr.close()
        self.consoles = []

    def shutdown(self):
        """ Shut the kernel down.

        Existing IPython consoles are killed first.
        """
        if self.ipkernel is not None:
            self.cleanup_consoles()
            self.ipkernel.close()
            # ipkernel.close is only registered for ipykernel 5.1.2 and later,
            # but unregistering something that wasn't registered is safe.
            atexit_unregister(self.ipkernel.close)
            self.ipkernel = None

            # Remove stored singleton to facilitate garbage collection.
            IPKernelApp.clear_instance()
