""" This code has been inspired from the IPython repository

https://github.com/ipython/ipython/blob/2.x/examples/Embedding/internal_ipkernel.py

"""
from __future__ import absolute_import, print_function, unicode_literals

import logging

import ipykernel.connect
import IPython.utils.io
import six

from envisage.plugins.ipython_kernel.kernelapp import IPKernelApp
from traits.api import Any, HasStrictTraits, Instance, List

logger = logging.getLogger(__name__)


# Replacements for IPython.utils.io.raw_print and IPython.utils.raw_print_err
# that send output to logging instead of to __stdout__ and __stderr__.

def log_print(*args, **kw):
    """
    Logging replacement for IPython.utils.io.raw_print.
    Instead of printing to __stdout__, this function logs at INFO level.
    """
    message = six.StringIO()
    print(*args, sep=kw.get('sep', ' '), end=kw.get('end', '\n'),
          file=message)
    logger.info(message.getvalue())


def log_print_err(*args, **kw):
    """
    Logging replacement for IPython.utils.io.raw_print_err.
    Instead of printing to __stdout__, this function logs at WARNING level.
    """
    message = six.StringIO()
    print(*args, sep=kw.get('sep', ' '), end=kw.get('end', '\n'),
          file=message)
    logger.warning(message.getvalue())


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

    #: old values for IPython's raw_print and raw_print_err, so that
    #: they can be restored.
    _original_raw_print = Any()
    _original_raw_print_err = Any()

    def init_ipkernel(self, gui_backend):
        """ Initialize the IPython kernel.

        Parameters
        ----------
        gui_backend -- string
          The GUI mode used to initialize the GUI mode. For options, see
          the `ipython --gui` help pages.
        """
        # Replace IPython's raw_print and raw_print_err with versions that log.
        self._original_raw_print = IPython.utils.io.raw_print
        self._original_raw_print_err = IPython.utils.io.raw_print_err
        IPython.utils.io.raw_print = log_print
        IPython.utils.io.raw_print_err = log_print_err

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
            self.ipkernel.shutdown()
            self.ipkernel = None

            # Remove stored singleton to facilitate garbage collection.
            IPKernelApp.clear_instance()

            # Restore changes to the ctrl-c-message.
            if self._original_ctrl_c_message is not None:
                ipykernel.kernelapp._ctrl_c_message = (
                    self._original_ctrl_c_message)
                self._original_ctrl_c_message = None

            # Undo changes to raw_print and raw_print_err.
            if self._original_raw_print_err is not None:
                IPython.utils.io.raw_print_err = self._original_raw_print_err
                self._original_raw_print_err = None
            if self._original_raw_print is not None:
                IPython.utils.io.raw_print = self._original_raw_print
                self._original_raw_print = None
