""" This code has been inspired from the IPython repository

https://github.com/ipython/ipython/blob/2.x/examples/Embedding/internal_ipkernel.py

"""
import atexit
from distutils.version import StrictVersion as Version
import sys

import ipykernel
from ipykernel.connect import connect_qtconsole
from ipykernel.ipkernel import IPythonKernel
from ipykernel.kernelapp import IPKernelApp
from ipykernel.zmqshell import ZMQInteractiveShell
import IPython.utils.io
import six
from tornado import ioloop
import zmq

from traits.api import Any, HasStrictTraits, Instance, List

from envisage.plugins.ipython_kernel.heartbeat import Heartbeat

NEEDS_IOLOOP_PATCH = Version(ipykernel.__version__) >= Version('4.7.0')


# XXX Refactor to avoid the fragile subclassing of IPKernelApp.
# XXX Move this class to its own module.
# XXX Make sure no fds are being leaked *even* if we're keeping all
#     the relevant objects alive. We shouldn't be depending on reference-count
#     based cleanup to reclaim fds.
# XXX Can we double check that _all_ sockets created are being closed
#     explicitly, rather than as a result of refcounting?
# XXX Is anyone actually messing with the displayhook? Check!
# XXX By the time that the Shell stores the sys state (InteractiveShell.save_sys_module_state),
#     it's already been swapped out for something else. Why? Who's setting the sys
#     attributes *before* save_sys_module_state gets called, and why?
# XXX Check list of *all* objects for anything suspiciously IPython-like.
#     What's the delta between the zeroth run and the first?


if six.PY2:
    def atexit_unregister(func):
        # Replace the contents, not the list itself, in case anyone else
        # is keeping references to it.
        atexit._exithandlers[:] = list(
            handler for handler in atexit._exithandlers
            if not handler[0] == func
        )
else:
    from atexit import unregister as atexit_unregister


class PatchedIPKernelApp(IPKernelApp):
    """
    Patched version of the IPKernelApp, mostly to support clean shutdown.

    """
    # Override to use local Heartbeat class.
    heartbeat = Instance(Heartbeat, allow_none=True)

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

        # Remove the atexit handler that's registered.
        atexit_unregister(self.iopub_thread.stop)

        # self.iopub_thread._event_puller.stop_on_recv()
        # XXX Again, not unbinding. Problem?
        # self.iopub_thread._event_puller.close()

        # self.iopub_thread._pipe_in.stop_on_recv()
        # XXX Again, not unbinding. Problem?
        #self.iopub_thread._pipe_in.close()

        # Lots of auxiliary sockets for the IOPubThread. Should we
        # be closing these before or after ?

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

    def close_shell(self):
        # clean up and close the shell attached to the kernel
        shell = self.kernel.shell

        # Clean up script magics object, which is contained in a reference
        # cycle, and has a __del__ method, preventing its removal in Python 2.
        magics_manager = shell.magics_manager
        script_magics = magics_manager.registry["ScriptMagics"]

        script_magics.kill_bg_processes()
        atexit_unregister(script_magics.kill_bg_processes)

        script_magics.magics.clear()
        script_magics.shell = None
        script_magics.parent = None

        shell.history_manager.end_session()
        # The stop also cleans up the file connection.
        shell.history_manager.save_thread.stop()
        # Don't run again at process shutdown.
        atexit_unregister(shell.history_manager.save_thread.stop)
        # Rely on garbage collection to clean up the file connection.
        shell.history_manager.db.close()
        del shell.configurables[:]

        del shell.sys_excepthook
        del shell._orig_sys_module_state
        del shell._orig_sys_modules_main_mod

        # atexit_operations does:
        # - history_manager end session (called above)
        # - remove temp files and directories
        # - clear user namespaces
        # - run user shutdown hooks
        # Do we want to do all these things? Should we just call
        # atexit_operations directly?
        atexit_unregister(shell.atexit_operations)

    def close_heartbeat(self):
        # This should interrupt the zmq.device call.
        self.heartbeat.context.term()
        self.heartbeat.join()

    def init_heartbeat(self):
        """start the heart beating"""
        # Overridden from parent to use the local Heartbeat class.

        # heartbeat doesn't share context, because it mustn't be blocked
        # by the GIL, which is accessed by libzmq when freeing zero-copy messages
        hb_ctx = zmq.Context()
        self.heartbeat = Heartbeat(hb_ctx, (self.transport, self.ip, self.hb_port))
        self.hb_port = self.heartbeat.port
        self.log.debug("Heartbeat REP Channel on port: %i" % self.hb_port)
        self.heartbeat.start()

    def XXXXinit_heartbeat(self):
        # Temporarily override while debugging, to avoid creating the
        # heartbeat at all. To do: allow the heartbeat to be created,
        # then shut it down (along with its sockets and context).
        pass

    def patch_io(self):
        # Overridden to do nothing. Alternatively, we need to write
        # and call a corresponding function at teardown that undoes
        # the faulthandler monkeypatching.

        # Related: https://github.com/ipython/ipykernel/issues/91

        # Suggest that the appropriate fix for users of this class
        # is to make sure they enable faulthandler before the
        # IPython kernel does its sys magic.
        pass

    def configure_tornado_logger(self):
        # Overridden to do nothing.
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

    #: sys.stdin value at time kernel was started
    _original_stdin = Any()

    #: sys.stdout value at time kernel was started
    _original_stdout = Any()

    #: sys.stderr value at time kernel was started
    _original_stderr = Any()

    #: sys.excepthook value at time kernel was started
    _original_excepthook = Any()

    #: sys.displayhook value at time kernel was started
    _original_displayhook = Any()

    #: Original sys.modules["__main__"]
    _original_modules_main = Any()

    #: old value for the _ctrl_c_message, so that it can be restored
    _original_ctrl_c_message = Any()

    _original_ipython_utils_io_stdin = Any()
    _original_ipython_utils_io_stdout = Any()
    _original_ipython_utils_io_stderr = Any()

    def init_ipkernel(self, gui_backend):
        """ Initialize the IPython kernel.

        Parameters
        ----------
        gui_backend -- string
          The GUI mode used to initialize the GUI mode. For options, see
          the `ipython --gui` help pages.
        """
        # More global state modification.

        # XXX Add general save-and-restore machinery, that copes with the
        # case where (a) the attribute does not exist; (b) the attribute
        # does exist, but is None, and (c) the attribute does exist, but
        # is not None. Cleanup may need to actually delete an attribute
        # that didn't previously exist.
        self._original_ipython_utils_io_stdin = IPython.utils.io.stdin
        self._original_ipython_utils_io_stdout = IPython.utils.io.stdout
        self._original_ipython_utils_io_stderr = IPython.utils.io.stderr

        # The IPython kernel modifies sys.stdout and sys.stderr when started,
        # and doesn't currently provide a way to restore them. So we restore
        # them ourselves at shutdown.
        self._original_stdin = sys.stdin
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr

        # The IPython kernel also modifies the excepthook and displayhook;
        # store them here, restore them later.

        # XXX Move this code! The kernelapp itself should be responsible
        # for resetting these cleanly.
        self._original_excepthook = sys.excepthook
        self._original_displayhook = sys.displayhook
        self._original_modules_main = sys.modules["__main__"]

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

            # XXX It may not make sense to be calling this.
            # It puts an event on the event loop, but in our use-cases
            # the event loop isn't running at this point.
            # self.ipkernel.shell.exit_now = True
            self.ipkernel.cleanup_connection_file()

            atexit_unregister(self.ipkernel.cleanup_connection_file)

            # XXX not quite right; it's the shell that's messing with this.
            # XXX The upstream code doesn't use __main__ here; should we
            # be doing something different?
            kernel_sys_modules_main = sys.modules["__main__"]
            if kernel_sys_modules_main is not self._original_modules_main:
                sys.modules["__main__"] = self._original_modules_main
                self._original_modules_main = None

            kernel_excepthook = sys.excepthook
            if kernel_excepthook is not self._original_excepthook:
                # XXX Should also reset self._original_excepthook if
                # this if branch is *not* taken.
                sys.excepthook = self._original_excepthook
                self._original_excepthook = None

            kernel_displayhook = sys.displayhook
            if kernel_displayhook is not self._original_displayhook:
                sys.displayhook = self._original_displayhook
                self._original_displayhook = None

            # The stdout and stderr streams created by the kernel use the
            # IOPubThread, so we need to close them and restore the originals
            # before we shut down the thread. Without this, we get obscure
            # errors of the form "TypeError: heap argument must be a list".

            kernel_stderr = sys.stderr
            if kernel_stderr is not self._original_stderr:
                sys.stderr = self._original_stderr
                kernel_stderr.close()
                self._original_stderr = None

            kernel_stdout = sys.stdout
            if kernel_stdout is not self._original_stdout:
                sys.stdout = self._original_stdout
                kernel_stdout.close()
                self._original_stdout = None

            kernel_stdin = sys.stdin
            if kernel_stdin is not self._original_stdin:
                sys.stdin = self._original_stdin
                kernel_stdin.close()
                self._original_stdin = None

            self.ipkernel.close_shell()
            self.ipkernel.close_kernel()
            self.ipkernel.close_heartbeat()
            self.ipkernel.close_sockets()

            # The kernelapp has a session, shared with the kernel.
            # That session contains a reference back to its parent (the
            # kernelapp), keeping it alive.
            #
            # We can't easily delete the ipkernel's session, since it's
            # declared as not allowing None. (Neither `del self.ipkernel.session` nor `self.ipkernel.session = None` works.)
            # So we remove the link to the parent instead.
            self.ipkernel.session.parent = None

            # The kernel also has a parent, which we set back to None.
            self.ipkernel.kernel.parent = None

            self.ipkernel = None

            # Restore changes to the ctrl-c-message.
            if self._original_ctrl_c_message is not None:
                ipykernel.kernelapp._ctrl_c_message = (
                    self._original_ctrl_c_message)
                self._original_ctrl_c_message = None

            IPython.utils.io.stdout = self._original_ipython_utils_io_stdin
            IPython.utils.io.stderr = self._original_ipython_utils_io_stderr
            IPython.utils.io.stdin = self._original_ipython_utils_io_stdin

            self._original_ipython_utils_io_stdin = None
            self._original_ipython_utils_io_stdout = None
            self._original_ipython_utils_io_stderr = None

            # Remove singletons.
            ZMQInteractiveShell.clear_instance()
            IPythonKernel.clear_instance()
            PatchedIPKernelApp.clear_instance()
