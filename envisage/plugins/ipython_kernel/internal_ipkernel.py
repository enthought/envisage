""" This code has been inspired from the IPython repository

https://github.com/ipython/ipython/blob/2.x/examples/Embedding/internal_ipkernel.py

"""

from IPython.lib.kernel import connect_qtconsole
from IPython.kernel.zmq.kernelapp import IPKernelApp


def mpl_kernel(gui):
    """ Launch and return an IPython kernel with matplotlib support for the
    desired gui.

    """
    kernel = IPKernelApp.instance()
    kernel.initialize(['python', '--pylab=%s' % gui])
    return kernel


class InternalIPKernel(object):

    def init_ipkernel(self, backend):
        # Start IPython kernel with GUI event loop and mpl support
        self.ipkernel = mpl_kernel(backend)
        # To create and track active qt consoles
        self.consoles = []

        # This application will also act on the shell user namespace
        self.namespace = self.ipkernel.shell.user_ns

        # self.namespace['ipkernel'] = self.ipkernel  # dbg

    def new_qt_console(self, evt=None):
        """start a new qtconsole connected to our kernel"""
        return connect_qtconsole(
            self.ipkernel.connection_file, profile=self.ipkernel.profile
        )

    def cleanup_consoles(self, evt=None):
        for c in self.consoles:
            c.kill()

    def shutdown(self):
        self.cleanup_consoles()
        self.ipkernel.shell.exit_now = True
