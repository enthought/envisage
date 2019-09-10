import atexit

from ipykernel.kernelapp import IPKernelApp as UpstreamIPKernelApp
import six
import zmq

from envisage.plugins.ipython_kernel.heartbeat import Heartbeat


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


class IPKernelApp(UpstreamIPKernelApp):
    """
    Patched version of the IPKernelApp, mostly to support clean shutdown.

    """
    def init_heartbeat(self):
        """start the heart beating"""
        # Overridden from the parent to use the local Heartbeat class,
        # which allows clean shutdown.

        # heartbeat doesn't share context, because it mustn't be blocked
        # by the GIL, which is accessed by libzmq when freeing zero-copy
        # messages
        hb_ctx = zmq.Context()
        self.heartbeat = Heartbeat(hb_ctx, (self.transport, self.ip, self.hb_port))
        self.hb_port = self.heartbeat.port
        self.log.debug("Heartbeat REP Channel on port: %i" % self.hb_port)
        self.heartbeat.start()

    def shutdown(self):
        """
        Undo the effects of the initialize method:

        - free system resources
        - undo changes to global state
        """

        self.close_shell()
        self.close_kernel()
        self.close_heartbeat()
        self.close_sockets()

        self.cleanup_connection_file()
        atexit_unregister(self.cleanup_connection_file)


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
        # by the GIL, which is accessed by libzmq when freeing zero-copy
        # messages
        hb_ctx = zmq.Context()
        self.heartbeat = Heartbeat(hb_ctx, (self.transport, self.ip, self.hb_port))
        self.hb_port = self.heartbeat.port
        self.log.debug("Heartbeat REP Channel on port: %i" % self.hb_port)
        self.heartbeat.start()

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
