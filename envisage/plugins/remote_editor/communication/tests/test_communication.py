# -*- coding: utf-8 -*-
# Standard library imports
import os
import unittest
from time import sleep
from threading import Thread

# ETS imports
from traits.api import Int, Str

# Local imports
from envisage.plugins.remote_editor.communication.client import Client
from envisage.plugins.remote_editor.communication.server import Server
from envisage.plugins.remote_editor.communication.util import \
    get_server_port, LOCK_PATH

from envisage._compat import unicode_str


class TestClient(Client):

    command = Str
    arguments = Str

    error_count = Int(0)

    def handle_command(self, command, arguments):
        self.command = command
        self.arguments = arguments

    def _error_changed(self, error):
        if error:
            self.error_count += 1


class TestThread(Thread):

    def run(self):
        self.server = Server()
        self.server.init()
        self.server.main()


class CommunicationTestCase(unittest.TestCase):

    def setUp(self):
        """ Make sure no old lock files exist prior to run.
        """
        if os.path.exists(LOCK_PATH):
            os.remove(LOCK_PATH)

    def tearDown(self):
        """ Make sure no old lock files are left around.
        """
        if os.path.exists(LOCK_PATH):
            os.remove(LOCK_PATH)

    def testCommunication(self):
        """ Can the Server communicate with Clients and handle errors
            appropriately?
        """
        # Test server set up

        # Does the ping operation work when the Server is not running?
        self.assert_(not Server.ping(get_server_port()))

        # Set up server thread
        serverThread = TestThread()
        serverThread.setDaemon(True)
        serverThread.start()
        sleep(.5)
        self.assert_(os.path.exists(LOCK_PATH))

        # Test normal operation
        tmp = get_server_port()
        self.assert_(Server.ping(tmp))

        client1 = TestClient(self_type='client1', other_type='client2')
        client1.register()
        client2 = TestClient(self_type='client2', other_type='client1')
        client2.register()
        sleep(.5)
        self.assert_(not(client1.orphaned or client2.orphaned))

        client1.send_command("foo", "bar")
        sleep(.1)
        self.assertEqual(client2.command, "foo")
        self.assertEqual(client2.arguments, "bar")

        client1.send_command(unicode_str("Très"), "bien")
        sleep(.1)
        self.assertEqual(client2.command, unicode_str("Très"))
        self.assertEqual(client2.arguments, "bien")


        client1.unregister()
        sleep(.1)
        self.assert_(client1.orphaned and client2.orphaned)

        client1.register()
        sleep(.1)
        self.assert_(not(client1.orphaned or client2.orphaned))

        # Simulated breakage -- does the Server handle unexpected communication
        # failure?

        # Have client1 'die'. We send the dummy command to force its connection
        # loop to terminate after the call to 'stop'. (In Python we can't just
        # kill the thread, which is really what we want to do in this case.)
        client1._communication_thread.stop()
        sleep(.1)
        serverThread.server._send_to(client1._port, "dummy", "")
        sleep(.1)

        # The Server should inform client1 that it could not complete its
        # request
        client2.send_command("foo", "bar")
        sleep(.1)
        self.assert_(client2.orphaned)
        self.assertEqual(client2.error_count, 1)


if __name__ == '__main__':
    """ Run the unittest, but redirect the log to stderr for convenience.
    """
    import logging
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    logging.getLogger("communication").addHandler(console)
    unittest.main()
