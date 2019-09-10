""" This code has been inspired from the IPython repository

https://github.com/ipython/ipython/blob/2.x/examples/Embedding/internal_ipkernel.py

"""
from __future__ import absolute_import, print_function, unicode_literals

from distutils.version import StrictVersion as Version

import ipykernel
from ipykernel.connect import connect_qtconsole
from ipykernel.ipkernel import IPythonKernel
from ipykernel.zmqshell import ZMQInteractiveShell

from envisage.plugins.ipython_kernel.kernelapp import IPKernelApp
from traits.api import Any, HasStrictTraits, Instance, List


# XXX Refactor to avoid the fragile subclassing of IPKernelApp. (One day.)
# XXX Make sure no fds are being leaked *even* if we're keeping all
#     the relevant objects alive. We shouldn't be depending on reference-count
#     based cleanup to reclaim fds.
# XXX Can we double check that _all_ sockets created are being closed
#     explicitly, rather than as a result of refcounting?
# XXX Check list of *all* objects for anything suspiciously IPython-like.
#     What's the delta between the zeroth run and the first?
# XXX Consider avoiding the "instance" singleton stuff. Maybe save that
#     for the rewrite.
# XXX Move kernelapp related stuff from here to kernelapp.
# XXX Testing: verify that the displayhook, excepthook and other sys pieces
#     have been restored.
# XXX Testing: verify that IPython.utils.io unaltered (stdin, too)


def gui_kernel(gui_backend):
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

    #: old value for the _ctrl_c_message, so that it can be restored
    _original_ctrl_c_message = Any()

    def init_ipkernel(self, gui_backend):
        """ Initialize the IPython kernel.

        Parameters
        ----------
        gui_backend -- string
          The GUI mode used to initialize the GUI mode. For options, see
          the `ipython --gui` help pages.
        """
        # More global state modification.

        # Suppress the unhelpful "Ctrl-C will not work" message from the
        # kernelapp.
        self._original_ctrl_c_message = getattr(
            ipykernel.kernelapp, "_ctrl_c_message", None)
        if self._original_ctrl_c_message is not None:
            ipykernel.kernelapp._ctrl_c_message = ""

        # Start IPython kernel with GUI event loop support
        self.ipkernel = gui_kernel(gui_backend)

        # This application will also act on the shell user namespace
        self.namespace = self.ipkernel.shell.user_ns
        self.namespace.update(dict(self.initial_namespace))

    def new_qt_console(self):
        """ Start a new qtconsole connected to our kernel. """
        console = connect_qtconsole(self.ipkernel.connection_file,
                                    argv=['--no-confirm-exit'])
        self.consoles.append(console)
        return console

    def cleanup_consoles(self):
        """ Kill all existing consoles. """
        for c in self.consoles:
            c.kill()
            c.stdout.close()
            c.stderr.close()
        self.consoles = []

    def shutdown(self):
        """ Shutdown the kernel.

        Existing IPython consoles are killed first.
        """
        if self.ipkernel is not None:
            self.cleanup_consoles()

            self.ipkernel.shutdown()
            self.ipkernel = None

            # Restore changes to the ctrl-c-message.
            if self._original_ctrl_c_message is not None:
                ipykernel.kernelapp._ctrl_c_message = (
                    self._original_ctrl_c_message)
                self._original_ctrl_c_message = None

            # Remove singletons to facilitate garbage collection.
            ZMQInteractiveShell.clear_instance()
            IPythonKernel.clear_instance()
            IPKernelApp.clear_instance()
