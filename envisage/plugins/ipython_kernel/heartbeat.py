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

import zmq

from ipykernel.heartbeat import Heartbeat as UpstreamHeartbeat


class Heartbeat(UpstreamHeartbeat):
    """
    Modified from the upstream class to enable the thread to be shut down
    cleanly.
    """
    def run(self):
        try:
            super(Heartbeat, self).run()
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                self.socket.close()
            else:
                raise
