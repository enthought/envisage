"""
This module contains an extended version of the upstream ipykernel IPKernelApp.

The main reason for extending is to support clean shutdown.
"""
from __future__ import absolute_import, print_function, unicode_literals

import atexit
import logging
import os
import sys

import ipykernel.ipkernel
import ipykernel.kernelapp
import ipykernel.zmqshell
import IPython.utils.io
import six
import zmq

from envisage.plugins.ipython_kernel.heartbeat import Heartbeat


# The IPython machinery registers various atexit cleanup handlers. We
# need to be able to do cleanup *before* process exit time, and some
# of the registered handlers are not idempotent, and so cause errors
# at process exit time. Those handlers also interfere with timely garbage
# collection by holding onto references to otherwise dead objects. So we
# deliberately unregister all registered handlers.

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

# Sentinel object used to represent a missing attribute.
_MISSING = object()


class IPKernelApp(ipykernel.kernelapp.IPKernelApp):
    """
    Patched version of the IPKernelApp, mostly to support clean shutdown.
    """

    # Methods overridden from the base class ##################################

    def init_heartbeat(self):
        """start the heart beating

        Overridden from the base class in order to swap in our own
        Heartbeat class in place of the official one. Our Heartbeat class
        is modified to allow the heartbeat thread to be shut down cleanly.

        This override can be removed once we're on ipkernel 5.x.
        """
        # heartbeat doesn't share context, because it mustn't be blocked
        # by the GIL, which is accessed by libzmq when freeing zero-copy
        # messages
        hb_ctx = zmq.Context()
        self.heartbeat = Heartbeat(
            hb_ctx,
            (self.transport, self.ip, self.hb_port),
        )
        self.hb_port = self.heartbeat.port
        self.log.debug("Heartbeat REP Channel on port: %i" % self.hb_port)
        self.heartbeat.start()

    def patch_io(self):
        """Patch important libraries that can't handle sys.stdout forwarding.

        Overridden from the base class to do nothing.

        The base class method monkeypatches faulthandler so that calling
        faulthandler.enable() while streams are redirected doesn't fail.

        This override bypasses that patching. Users of the Envisage plugin
        are advised to enable faulthandler (if desired) as part of
        application setup, before the plugin is started.

        Related: https://github.com/ipython/ipykernel/issues/91
        """
        pass

    def configure_tornado_logger(self):
        """
        Configure tornado logging.

        Adds a NullHandler to the tornado root logger, if there are
        no handlers already present on that logger. If no tornado
        handler is present at the time the IO loop is started, tornado
        will call logging.basicConfig, which isn't what we want to happen.

        Overridden from the base class, which unconditionally adds a new
        StreamHandler every time.

        See also:
        - https://github.com/tornadoweb/tornado/blob/v6.0.3/tornado/ioloop.py#L427-L445  # noqa: E501
        - https://github.com/tornadoweb/tornado/pull/741
        """
        logger = logging.getLogger("tornado")
        if not logger.handlers:
            logger.addHandler(logging.NullHandler())

    def log_connection_info(self):
        """
        Display connection info, and store ports.

        Overridden to not write information to __stdout__. We don't usually
        want this in applications that embed an IPython kernel (as opposed
        to the case where IPython effectively *is* the application).
        """
        basename = os.path.basename(self.connection_file)
        if (basename == self.connection_file or
                os.path.dirname(self.connection_file) == self.connection_dir):
            # use shortname
            tail = basename
        else:
            tail = self.connection_file
        lines = [
            "To connect another client to this kernel, use:",
            "    --existing %s" % tail,
        ]
        # log connection info
        # info-level, so often not shown.
        # frontends should use the %connect_info magic
        # to see the connection info
        for line in lines:
            self.log.info(line)

        self.ports = dict(
            shell=self.shell_port,
            iopub=self.iopub_port,
            stdin=self.stdin_port,
            hb=self.hb_port,
            control=self.control_port,
        )

    # Methods extending the base class methods ################################

    def init_crash_handler(self):
        """
        Set up a suitable exception hook.

        Extended to keep track of the original sys.excepthook value, so that it
        can be restored later.
        """
        self._original_sys_excepthook = sys.excepthook
        super(IPKernelApp, self).init_crash_handler()

    def init_io(self):
        """
        Redirect input streams and set a display hook.

        Extended to store the original sys attributes so that they
        can be restored later.
        """
        if self.outstream_class:
            self._original_sys_stdout = sys.stdout
            self._original_sys_stderr = sys.stderr

        if self.displayhook_class:
            self._original_sys_displayhook = sys.displayhook

        super(IPKernelApp, self).init_io()

    def init_kernel(self):
        """
        Create the kernel object itself.

        Extended to store the original values of IPython.utils.io.stdout
        and IPython.utils.io.stderr, so that they can be restored later.
        """
        self._original_ipython_utils_io_stdout = getattr(
            IPython.utils.io, "stdout", _MISSING)
        self._original_ipython_utils_io_stderr = getattr(
            IPython.utils.io, "stderr", _MISSING)
        super(IPKernelApp, self).init_kernel()

    # New methods, mostly to control shutdown #################################

    def close(self):
        """
        Undo the effects of the initialize method:

        - free resources allocated during initialization
        - undo changes to global state
        """
        # Note: the upstream ipykernel introduced its own close method in
        # v5.1.2, along with an atexit handler for that method. See
        # https://github.com/ipython/ipykernel/pull/412. For ipykernel versions
        # of 5.1.2 or later, this method overrides the base class version.
        self.close_shell()
        self.close_kernel()
        self.close_io()
        self.close_heartbeat()
        self.close_sockets()

        self.cleanup_connection_file()
        atexit_unregister(self.cleanup_connection_file)

        self.close_crash_handler()
        self.close_profile_dir()
        self.cleanup_singletons()

    def close_shell(self):
        """
        Clean up resources allocated by the shell.
        """
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

        # The shell's cleanup method restores the sys.module changes.
        shell.cleanup()

        # The atexit_operations method ends the history manager session,
        # but doesn't stop the history manager's save_thread, so we need
        # to do that separately.
        shell.atexit_operations()
        atexit_unregister(shell.atexit_operations)

        shell.history_manager.save_thread.stop()
        atexit_unregister(shell.history_manager.save_thread.stop)

        # Rely on garbage collection to clean up the file connection.
        shell.history_manager.db.close()

        # Remove some references to avoid keeping objects alive unnecessarily.
        del shell.configurables[:]
        del shell.sys_excepthook
        del shell._orig_sys_module_state
        del shell._orig_sys_modules_main_mod

    def close_kernel(self):
        """
        Undo setup from init_kernel.
        """
        # Unhook listeners, and close kernel streams (which also closes
        # the corresponding zmq.Socket objects).
        kernel = self.kernel
        while kernel.shell_streams:
            stream = kernel.shell_streams.pop()
            stream.stop_on_recv()
            stream.close()

        # Remove selected references to allow effective garbage collection.
        kernel.stdin_socket = None

        # Undo changes to IPython.utils.io made at shell creation time.
        # The values written by the shell keep references that prevent
        # proper garbage collection from taking place.
        if self._original_ipython_utils_io_stderr is _MISSING:
            del IPython.utils.io.stderr
        else:
            IPython.utils.io.stderr = self._original_ipython_utils_io_stderr
        del self._original_ipython_utils_io_stderr

        if self._original_ipython_utils_io_stdout is _MISSING:
            del IPython.utils.io.stdout
        else:
            IPython.utils.io.stdout = self._original_ipython_utils_io_stdout
        del self._original_ipython_utils_io_stdout

    def close_io(self):
        """
        Undo the effects of init_io.

        Restores sys module attributes altered by init_io.
        """
        if self.displayhook_class:
            sys.displayhook = self._original_sys_displayhook
            del self._original_sys_displayhook

        if self.outstream_class:
            sys.stderr.close()
            sys.stderr = self._original_sys_stderr
            del self._original_sys_stderr

            sys.stdout.close()
            sys.stdout = self._original_sys_stdout
            del self._original_sys_stdout

    def close_iopub(self):
        """
        Close iopub-related resources.
        """
        iopub_socket = self.iopub_thread.socket

        # Remove the atexit handler that's registered.
        self.iopub_thread.stop()
        atexit_unregister(self.iopub_thread.stop)

        iopub_socket.close()

    def close_crash_handler(self):
        """
        Undo the global state change from init_crash_handler.

        Restore the sys.excepthook attribute.
        """
        sys.excepthook = self._original_sys_excepthook
        del self._original_sys_excepthook

    def close_heartbeat(self):
        """
        Stop the heartbeat thread, by terminating the corresponding
        zmq.Context.
        """
        # This should interrupt the zmq.device call.
        self.heartbeat.context.term()
        self.heartbeat.join()

    def close_sockets(self):
        """
        Unbind, close and destroy sockets created by init_sockets.
        """
        self.close_iopub()

        for channel in ('shell', 'control', 'stdin'):
            self.log.debug("Closing %s channel", channel)
            socket = getattr(self, channel + "_socket", None)
            if socket and not socket.closed:
                socket.close()

        # ipykernel 5.1.2 and later creates its own context. Earlier versions
        # use the shared zmq context. Ref: ipython/ipykernel#412.
        if hasattr(self, "context"):
            self.log.debug("Terminating zmq context")
            self.context.term()
            self.log.debug("Terminated zmq context")

    def close_profile_dir(self):
        """
        Undo changes made in init_profile_dir.
        """
        ipython_dir_entry = os.path.abspath(self.ipython_dir)
        if ipython_dir_entry in sys.path:
            sys.path.remove(ipython_dir_entry)

    def cleanup_singletons(self):
        """
        Clear SingletonConfigurable instances.
        """
        # These instances will otherwise hinder garbage collection,
        # and prevent a clean recreation of a new kernel app.
        ipykernel.zmqshell.ZMQInteractiveShell.clear_instance()
        ipykernel.ipkernel.IPythonKernel.clear_instance()
