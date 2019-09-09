"""The client and server for a basic ping-pong style heartbeat.
"""

# This is a copy of the upstream ipykernel v4.10.1 code from:
#
#   https://github.com/ipython/ipykernel/blob/v4.10.1/ipykernel/heartbeat.py
#
# modified so that the Heartbeat run method catches an attempt to terminate
# the context and closes the relevant socket, along the lines of the code
# here:
#
#   https://github.com/ipython/ipykernel/blob/master/ipykernel/heartbeat.py#L103-L111
#
# This provides a way to shut down the heartbeat thread externally.


#-----------------------------------------------------------------------------
#  Copyright (C) 2008-2011  The IPython Development Team
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

import errno
import os
import socket
from threading import Thread

import zmq

from jupyter_client.localinterfaces import localhost

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------


class Heartbeat(Thread):
    "A simple ping-pong style heartbeat that runs in a thread."

    def __init__(self, context, addr=None):
        if addr is None:
            addr = ('tcp', localhost(), 0)
        Thread.__init__(self)
        self.context = context
        self.transport, self.ip, self.port = addr
        if self.port == 0:
            if addr[0] == 'tcp':
                s = socket.socket()
                # '*' means all interfaces to 0MQ, which is '' to socket.socket
                s.bind(('' if self.ip == '*' else self.ip, 0))
                self.port = s.getsockname()[1]
                s.close()
            elif addr[0] == 'ipc':
                self.port = 1
                while os.path.exists("%s-%s" % (self.ip, self.port)):
                    self.port = self.port + 1
            else:
                raise ValueError("Unrecognized zmq transport: %s" % addr[0])
        self.addr = (self.ip, self.port)
        self.daemon = True

    def run(self):
        self.socket = self.context.socket(zmq.ROUTER)
        self.socket.linger = 1000
        c = ':' if self.transport == 'tcp' else '-'
        self.socket.bind('%s://%s' % (self.transport, self.ip) + c + str(self.port))
        while True:
            try:
                zmq.device(zmq.QUEUE, self.socket, self.socket)
            except zmq.ZMQError as e:
                if e.errno == errno.EINTR:
                    continue
                elif e.errno == zmq.ETERM:
                    self.socket.close()
                    break
                else:
                    raise
            else:
                break
