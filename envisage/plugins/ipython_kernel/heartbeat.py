# (C) Copyright 2019-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
"""
A simple ping-pong style heartbeat that runs in a thread.

Modified from upstream to enable the heartbeat thread to be shut down cleanly.
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
#
# Once we're using ipykernel 5.x, this module can be removed and we can
# revert to using the upstream Heartbeat class.

import ipykernel.heartbeat
import zmq


class Heartbeat(ipykernel.heartbeat.Heartbeat):
    """
    A simple ping-pong style heartbeat that runs in a thread.

    Modified from upstream to enable the thread to be shut down cleanly.
    """

    def run(self):
        try:
            super().run()
        except zmq.ZMQError as e:
            # We expect to get here on normal context termination, but
            # not otherwise; re-raise if the error is not the expected one
            # (but close the socket anyway, to allow the context termination
            # to complete without blocking the main thread).
            self.socket.close()
            if e.errno != zmq.ETERM:
                raise
