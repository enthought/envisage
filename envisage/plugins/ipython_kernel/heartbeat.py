"""
The client and server for a basic ping-pong style heartbeat.
"""

# We're currently using ipykernel v4.10.1. In that version, there's no way to
# cleanly shut down the Heartbeat thread. However, ipykernel v5.x allows the
# thread to be shut down by terminating the corresponding context. The relevant
# code is here:
#
#   https://github.com/ipython/ipykernel/blob/18f2ef77b6a72109a1e50d8229e7216f1cfc2e39/ipykernel/heartbeat.py#L103-L111
#
# The key change is to explicitly catch the termination attempt and close
# the socket. Without this, the Context.term call from the main thread
# will hang: the open socket prevents termination.
#
# This version of Heartbeat subclasses the upstream version to introduce the
# minimal changes necessary to make shutdown feasible with the v4.10.1 code.

import zmq

from ipykernel.heartbeat import Heartbeat as UpstreamHeartbeat


class Heartbeat(UpstreamHeartbeat):
    """
    A simple ping-pong style heartbeat that runs in a thread.

    Modified from upstream to enable the thread to be shut down cleanly.
    """
    def run(self):
        try:
            super(Heartbeat, self).run()
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                self.socket.close()
            else:
                raise
