""" This code has been inspired from the IPython repository

https://github.com/ipython/ipython/blob/2.x/examples/Embedding/internal_ipkernel.py

"""
from distutils.version import StrictVersion as Version
import sys

import ipykernel
from ipykernel.connect import connect_qtconsole
from ipykernel.ipkernel import IPythonKernel
from ipykernel.kernelapp import IPKernelApp
from tornado import ioloop

from traits.api import Any, HasStrictTraits, Instance, List

NEEDS_IOLOOP_PATCH = Version(ipykernel.__version__) >= Version('4.7.0')


# XXX Refactor to avoid the fragile subclassing of IPKernelApp.
# XXX Move this class to its own module.

class PatchedIPKernelApp(IPKernelApp):
    """
    Patched version of the IPKernelApp, mostly to support clean shutdown.

    """
    def _unbind_socket(self, s, port):
        transport = self.transport

        if port <= 0:
            # This should only happen if _bind_socket hasn't been called.
            # So we shouldn't ever get here, but perhaps we should defensively
            # do nothing (maybe print a warning about unbinding a port
            # that was never bound) if we do get here.
            raise RuntimeError("Shouldn't ever get here.")

        # XXX Repetition of information from _bind_socket; refactor
        # to remove the repetition.
        if transport == "tcp":
            endpoint = "tcp://%s:%i" % (self.ip, port)
        elif transport == "ipc":
            endpoint = "ipc://%s-%i" % (self.ip, port)
        else:
            raise ValueError(
                "Unknown transport type: {}".format(self.transport))

        s.unbind(endpoint)

    def close_sockets(self):
        """
        Unbind, close and destroy sockets created by init_sockets.
        """
        # context = zmq.Context.instance()
        self.close_iopub()

        # XXX Already closed by close_kernel, but not explictly unbound.
        # unbind after close fails (not surprisingly)
        # Do we still need to unbind?
        #self._unbind_socket(self.control_socket, self.control_port)
        #self.control_socket.close()
        del self.control_socket

        self._unbind_socket(self.stdin_socket, self.stdin_port)
        self.stdin_socket.close()
        del self.stdin_socket

        # Also already closed when closing the associated ZMQStream
        #self._unbind_socket(self.shell_socket, self.shell_port)
        #self.shell_socket.close()
        del self.shell_socket

    def close_iopub(self):
        """
        Close iopub-related resources.
        """
        self.iopub_socket = self.iopub_thread.socket
        self.iopub_thread.stop()

        self._unbind_socket(self.iopub_socket, self.iopub_port)
        self.iopub_socket.close()
        del self.iopub_socket

    def close_kernel(self):
        """
        Undo setup from init_kernel.
        """
        # Dig in to find the shell stream and control stream.
        # kernel is a an IPythonKernel object

        # XXX This is ugly: ideally, we should be closing the streams
        # in the same class that creates them. That may be awkward
        # in practice.
        kernel = self.kernel
        for stream in kernel.shell_streams:
            stream.stop_on_recv()
            # This also closes the corresponding socket.
            stream.close()

    def init_heartbeat(self):
        # Temporarily override while debugging, to avoid creating the
        # heartbeat at all. To do: allow the heartbeat to be created,
        # then shut it down (along with its sockets and context).
        pass





def gui_kernel(gui_backend):
    """ Launch and return an IPython kernel GUI with support.

    Parameters
    ----------
    gui_backend -- string or None
      The GUI mode used to initialize the GUI mode. For options, see
      the `ipython --gui` help pages. If None, the kernel is initialized
      without GUI support.
    """

    kernel = PatchedIPKernelApp.instance()

    argv = ['python']
    if gui_backend is not None:
        argv.append('--gui={}'.format(gui_backend))
    kernel.initialize(argv)

    return kernel


class InternalIPKernel(HasStrictTraits):
    """ Represents an IPython kernel and the consoles attached to it.
    """

    #: The IPython kernel.
    ipkernel = Instance(PatchedIPKernelApp)

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
        # The IPython kernel modifies sys.stdout and sys.stderr when started,
        # and doesn't currently provide a way to restore them. So we restore
        # them ourselves at shutdown.
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr

        # Suppress the unhelpful "Ctrl-C will not work" message from the
        # kernelapp.
        self._original_ctrl_c_message = getattr(
            ipykernel.kernelapp, "_ctrl_c_message", None)
        if self._original_ctrl_c_message is not None:
            ipykernel.kernelapp._ctrl_c_message = ""

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
            c.stdout.close()
            c.stderr.close()
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

            self.ipkernel.close_kernel()
            self.ipkernel.close_sockets()
            self.ipkernel = None

            # Restore changes to the ctrl-c-message.
            if self._original_ctrl_c_message is not None:
                ipykernel.kernelapp._ctrl_c_message = (
                    self._original_ctrl_c_message)
                self._original_ctrl_c_message = None

            # Remove singletons.
            PatchedIPKernelApp.clear_instance()
            IPythonKernel.clear_instance()
