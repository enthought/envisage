""" This code has been inspired from the IPython repository

https://github.com/ipython/ipython/blob/2.x/examples/Embedding/internal_ipkernel.py

"""
from ipykernel.connect import connect_qtconsole
from ipykernel.kernelapp import IPKernelApp

from traits.api import Any, HasStrictTraits, Instance, List


def mpl_kernel(gui_backend):
    """ Launch and return an IPython kernel with matplotlib support.

    Parameters
    ----------
    gui_backend -- string or None
      The GUI mode used to initialize the matplotlib mode. For options, see
      the `ipython --matplotlib` help pages. If None, the kernel is initialized
      without GUI support.
    """

    kernel = IPKernelApp.instance()

    argv = ['python']
    if gui_backend is not None:
        argv.append('--matplotlib={}'.format(gui_backend))
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

    def init_ipkernel(self, gui_backend):
        """ Initialize the IPython kernel.

        Parameters
        ----------
        gui_backend -- string
          The GUI mode used to initialize the matplotlib mode. For options, see
          the `ipython --matplotlib` help pages.
        """
        # Start IPython kernel with GUI event loop and mpl support
        self.ipkernel = mpl_kernel(gui_backend)

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
            self.ipkernel = None
