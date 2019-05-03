""" This code has been inspired from the IPython repository

https://github.com/ipython/ipython/blob/2.x/examples/Embedding/internal_ipkernel.py

"""
from distutils.version import StrictVersion as Version
import sys

import ipykernel
from ipykernel.connect import connect_qtconsole
from ipykernel.kernelapp import IPKernelApp
from tornado import ioloop

from traits.api import Any, HasStrictTraits, Instance, List

NEEDS_IOLOOP_PATCH = Version(ipykernel.__version__) >= Version('4.7.0')


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

    #: sys.stdout value at time kernel was started
    _original_stdout = Any()

    #: sys.stderr value at time kernel was started
    _original_stderr = Any()

    def init_ipkernel(self, gui_backend):
        """ Initialize the IPython kernel.

        Parameters
        ----------
        gui_backend -- string
          The GUI mode used to initialize the GUI mode. For options, see
          the `ipython --gui` help pages.
        """
        # The IPython kernel modifies sys.stdout and sys.stderr when started,
        # and doesn't currently provide a way to restore them. So we restore
        # them ourselves at shutdown.
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr

        # Start IPython kernel with GUI event loop support
        self.ipkernel = gui_kernel(gui_backend)

        # Since ipykernel 4.7, the io_loop attribute of the kernel is not
        # initialized anymore
        # Reference: https://github.com/enthought/envisage/issues/107
        # Workaround: Retrieve the kernel on the IPykernelApp and set the
        # io_loop without starting it!
        if NEEDS_IOLOOP_PATCH and not hasattr(self.ipkernel.kernel, 'io_loop'):
            self.ipkernel.kernel.io_loop = ioloop.IOLoop.instance()

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
        self.consoles = []

    def shutdown(self):
        """ Shutdown the kernel.

        Existing IPython consoles are killed first.
        """
        if self.ipkernel is not None:
            self.cleanup_consoles()
            self.ipkernel.shell.exit_now = True
            self.ipkernel.cleanup_connection_file()

            # The stdout and stderr streams created by the kernel use the
            # IOPubThread, so we need to close them and restore the originals
            # before we shut down the thread. Without this, we get obscure
            # errors of the form "TypeError: heap argument must be a list".
            kernel_stdout = sys.stdout
            if kernel_stdout is not self._original_stdout:
                sys.stdout = self._original_stdout
                kernel_stdout.close()

            kernel_stderr = sys.stderr
            if kernel_stderr is not self._original_stderr:
                sys.stderr = self._original_stderr
                kernel_stderr.close()

            self.ipkernel.iopub_thread.stop()
            self.ipkernel = None
