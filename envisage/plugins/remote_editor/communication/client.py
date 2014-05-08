# Standard library imports
import logging
import os
import select
import socket
import sys
from threading import Thread

# ETS imports
from traits.api import HasTraits, Int, Str, Bool, Instance, List, \
     Tuple, Enum
from envisage.plugins import remote_editor

# Local imports
from .server import Server
from .util import accept_no_intr, get_server_port, receive, send_port, \
    spawn_independent, MESSAGE_SEP

logger = logging.getLogger(__name__)


class ClientThread(Thread):
    """ A thread for listening for commands from the server.
    """

    def __init__(self, client):
        Thread.__init__(self)
        self.client = client
        self._finished = False

    def run(self):
        # Get the server port, spawning it if necessary
        server_port = get_server_port()
        if server_port == -1 or not Server.ping(server_port, timeout=5):
            if len(self.client.server_prefs):
                # Spawn the server
                logger.info("Client spawning Server...")
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.bind(('localhost', 0))
                sock.listen(1)
                port = sock.getsockname()[1]
                args = self.client.server_prefs + ( port, )
                code = "from envisage.plugins.remote_editor.communication." \
                    "server import main; main(r'%s', '%s', %i)" % args
                spawn_independent([sys.executable, '-c', code])

                # Await a reponse from the server
                try:
                    server, address = accept_no_intr(sock)
                    try:
                        command, arguments = receive(server)
                        if command == "__port__":
                            self.client._server_port = int(arguments)
                        else:
                            raise socket.error
                    finally:
                        # Use try...except to handle timeouts
                        try:
                            server.shutdown(socket.SHUT_RD)
                        except:
                            pass
                except socket.error as e:
                    logger.error(repr(e))
                    logger.error("Client spawned a non-responsive Server! " \
                                     "Unregistering...")
                    self.client.error = True
                    self.client.unregister()
                    return
                finally:
                    sock.close()

            else:
                logger.error("Client could not contact the Server and no " \
                                 "spawn command is defined. Unregistering...")
                self.client.error = True
                self.client.unregister()
                return
        else:
            self.client._server_port = server_port

        # Create the socket that will receive commands from the server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 0))
        sock.listen(1)
        self.client._port = sock.getsockname()[1]

        # Register with the server
        port = str(self.client._port)
        arguments = MESSAGE_SEP.join((port, self.client.self_type,
                                      self.client.other_type))
        self.client.error = not send_port(self.client._server_port, 'register',
                                          arguments)
        self.client.registered = True

        # Send queued commands (these can only exist if we spawned the server)
        for command, args in self.client._queue:
            arguments = MESSAGE_SEP.join((port, command, args))
            self.client.error = not send_port(self.client._server_port, 'send',
                                              arguments)
        self.client._queue = []

        # Start the loop to listen for commands from the Server
        logger.info("Client listening on port %i..." % self.client._port)
        try:
            while not self._finished:
                server, address = accept_no_intr(sock)

                # Reject non-local connections
                if address[0] != '127.0.0.1':
                    msg = "Client on port %s received connection from a " \
                        "non-local party (port %s). Ignoring..."
                    logger.warning(msg % (port, address[0]))
                    continue

                # Receive the command from the server
                self.client.error = False
                command, arguments = receive(server)
                msg = r"Client on port %s received: %s %s"
                logger.debug(msg, port, command, arguments)

                # Handle special commands from the server
                if command == "__orphaned__":
                    self.client.orphaned = bool(int(arguments))

                elif command == "__error__":
                    error_status = arguments[0]
                    error_message = ''
                    if len(arguments) > 0:
                        error_message = arguments[1:]
                    logger.warning("Error status received from the server: " \
                                       "%s\n%s" % (error_status, error_message))
                    self.client.error = bool(int(error_status))

                # Handle other commands through Client interface
                else:
                    if self.client.ui_dispatch == 'off':
                        self.client.handle_command(command, arguments)
                    else:
                        if self.client.ui_dispatch == 'auto':
                            from pyface.gui import GUI
                        else:
                            exec('from pyface.ui.%s.gui import GUI' %
                                 self.client.ui_dispatch)
                        GUI.invoke_later(self.client.handle_command,
                                         command, arguments)
        finally:
            self.client.unregister()

    def stop(self):
        self._finished = True


class Client(HasTraits):
    """ An object that communicates with another object through a Server.
    """

    # The preferences file path and node path to use for spawning a Server. If
    # this is not specified it will not be possible for this Client to spawn
    # the server.
    server_prefs = Tuple((os.path.join(remote_editor.__path__[0],
                                       "preferences.ini"),
                          "enthought.remote_editor"),
                         Str, Str)

    # The type of this object and the type of the desired object, respectively
    self_type = Str
    other_type = Str

    # Specifies how 'handle_command' should be called. If 'auto', use the
    # dispatch method appropriate for the toolkit Traits is using. Failure to
    # set this variable as appropriate will likely result in crashes.
    ui_dispatch = Enum('off', 'auto', 'wx', 'qt4')

    # Whether this client has been registered with the Server. Note that this is
    # *not* set after the 'register' method is called--it is set when the Server
    # actually receives the register command, which happens asynchronously.
    registered = Bool(False)

    # The client's orphaned status
    orphaned = Bool(True)

    # The client's error state. This is set to True after a failure to
    # communicate with the server or a failure by the server to communicate with
    # this object's counterpart.
    error = Bool(False)

    # Protected traits
    _port = Int
    _server_port = Int
    _communication_thread = Instance(ClientThread)
    _queue = List(Tuple(Str, Str))

    def register(self):
        """ Inform the server that this Client is available to receive
            commands.
        """
        if self._communication_thread is not None:
            raise RuntimeError("'register' has already been called on Client!")

        self._communication_thread = ClientThread(self)
        self._communication_thread.setDaemon(True)
        self._communication_thread.start()

    def unregister(self):
        """ Inform the server that this Client is no longer available to receive
            commands. Note that it is poor etiquette not to communicate when a
            Client is becoming unavailable. Calling 'unregister' when a Client
            is not registered has no effect.
        """
        if self._communication_thread is not None:
            self._communication_thread.stop()
            self._communication_thread = None
            send_port(self._server_port, 'unregister', str(self._port))
            self._port = 0
            self._server_port = 0
            self.registered = False
            self.orphaned = True

    def send_command(self, command, arguments=''):
        """ Send a command to the server which is to be passed to an object
            of the appropriate type.
        """
        if self._communication_thread is None:
            raise RuntimeError("Client is not registered. Cannot send command.")

        msg = r"Client on port %i sending: %s %s"
        logger.debug(msg, self._port, command, arguments)

        args = MESSAGE_SEP.join((str(self._port), command, arguments))
        if self.registered:
            self.error = not send_port(self._server_port, 'send', args)
        else:
            self._queue.append((command, arguments))

    def handle_command(self, command, arguments):
        """ This function should take a command string and an arguments string
            and do something with them. It should return True if the command
            given was understood; otherwise, False.
        """
        raise NotImplementedError()




