# Standard library imports
import logging
import sys
import os
import socket
from threading import Thread

# ETS imports
from enthought.traits.api import HasTraits, Int, Str, Bool, Instance, List, \
     Tuple
from enthought.plugins import remote_editor


# Local imports
from server import Server
from util import get_server_port, recieve, send_port, spawn_independent, \
     MESSAGE_SEP

logger = logging.getLogger(__name__)

class ClientThread(Thread):
    """ A thread for listening for commands from the server.
    """
    finished = False

    def __init__(self, client):
        Thread.__init__(self)
        self.client = client

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
                code = "from enthought.plugins.remote_editor.communication.server import main;"
                code += "main(r'%s', '%s', %i)" % args
                spawn_independent([sys.executable, '-c', code])

                # Await a reponse from the server
                try:
                    server, address = sock.accept()
                    try:
                        command, arguments = recieve(server)
                        if command == "__port__":
                            self.client._server_port = int(arguments)
                        else:
                            sock.shutdown(socket.SHUT_RD)
                            raise socket.error
                    finally:
                        # use try..except to handle timeouts.
                        try:
                            server.shutdown(socket.SHUT_RD)
                        except:
                            pass
                except socket.error:
                    logger.error("Client spawned a non-responsive Server! Unregistering...")
                    self.client.error = True
                    self.client.unregister()
                    return
                    
            else:
                logger.error("Client could not contact the Server and no spawn command is defined. Unregistering...")
                self.client.error = True
                self.client.unregister()
                return
        else:
            self.client._server_port = server_port

        # Create the socket that will recieve commands from the server
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
        
        # Send queued commands (these only can exist if we spawned the server)
        for command, arguments in self.client._queue:
            self.client.error = not send_port(self.client._server_port,
                                              command, arguments)
        self.client._queue = []

        # Start the loop to listen for commands from the Server
        logger.info("Client listening on port %i..." % self.client._port)
        try:
            try:
                while not self.finished:
                    server, address = sock.accept()
                    if address[0] != '127.0.0.1':
                        msg = "Client on port %s recieved connection from a non-local party (port %s). Ignoring..."
                        logger.warning(msg % (port, address[0]))
                        continue
                    self.client.error = False
                    command, arguments = recieve(server)
                    msg = "Client on port %s recieved: %s %s"
                    logger.info(msg, port, command, arguments)
                    if command == "__orphaned__":                        
                        self.client.orphaned = bool(int(arguments))
                    elif command == "__error__":
                        error_status = arguments[0]
                        error_message =''
                        if len(arguments) > 0:
                            error_message = arguments[1:]
                        logger.warning(
                            "Error status recieved from the server: %s\n%s"
                                    % (error_status, error_message))
                        self.client.error = bool(int(error_status))
                    else:
                        if self.client.wx:
                            import wx
                            wx.CallAfter(self.client.handle_command, command,
                                        arguments)
                        else:
                            self.client.handle_command(command, arguments)
            finally:
                if hasattr(self, 'client'):
                    self.client.unregister()
        finally:
            sock.shutdown(socket.SHUT_RD)

    def stop(self):
        self.finished = True
        

class Client(HasTraits):
    """ An object that communicates with another object through a Server.
    """

    # The preferences file path and node path to use for spawning a Server.
    # If this is not specified it will not be possible for this Client,
    # to spawn the server.
    server_prefs = Tuple((os.path.join(remote_editor.__path__[0], 
                                "preferences.ini"),
                                "enthought.remote_editor"),
                         Str, Str)

    # The type of this object and the type of the desired object, respectively
    self_type = Str
    other_type = Str

    # Whether or not this client will be contained in a wx application. Failure
    # to set this variable when appropriate will likely result in crashes.
    wx = Bool(False)

    # Whether this client has been registered with the Server. Note that this
    # is *not* set after the 'register' method is called--it is set when the
    # Server actually recieves the register command, which happens
    # asynchronously.
    registered = Bool(False)

    # The client's orphaned status
    orphaned = Bool(True)

    # The client's error state (this is set to True after a failure to
    # communicate with the server, or a failure on the server's part to
    # communicate with this object's counterpart).
    error = Bool(False)

    # Protected traits
    _port = Int
    _server_port = Int
    _communication_thread = Instance(ClientThread)
    _queue = List(Tuple(Str, Str))

    def register(self):
        """ Inform the server that this Client is available to recieve
            commands.
        """
        if self._communication_thread is not None:
            raise RuntimeError, "Register has already been called on this Client!"
        self._communication_thread = ClientThread(self)
        self._communication_thread.setDaemon(True)
        self._communication_thread.start()

    def unregister(self):
        """ Inform the server that this Client is no longer available to
            recieve commands. Note that it is poor etiquette not to
            communicate when a Client is becoming unavailable. Calling
            'unregister' when a Client is not registered has no effect.
        """
        if self._communication_thread is None:
            return
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
        args = MESSAGE_SEP.join((str(self._port), command, arguments))
        if self.registered:
            self.error = not send_port(self._server_port, 'send', args)
        else:
            self._queue.append(('send', args))
        
    def handle_command(self, command, arguments):
        """ This function should take a command string and an arguments
            string and do something with them. It should return True if
            the command given was understood; otherwise, False.
        """
        raise NotImplementedError

            

            
