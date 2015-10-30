# Standard library imports
import os, sys
import logging
import socket

# ETS imports
from apptools.preferences.api import Preferences
from traits.api import HasTraits, HasStrictTraits, Int, Str, List, \
     Dict, Tuple, Instance

# Local imports
from .util import accept_no_intr, receive, send_port, spawn_independent, \
    MESSAGE_SEP, LOCK_PATH, LOG_PATH

logger = logging.getLogger("communication")
logger.setLevel(logging.DEBUG)
logging.basicConfig(filename=LOG_PATH)


class PortInfo(HasStrictTraits):
    """ Object to store information on how a port is being used.
    """
    port = Int
    type = Str
    other_type = Str

    def __str__(self):
        return "Port: %i, Type: %s, Other type: %s" % \
            (self.port, self.type, self.other_type)


class Server(HasTraits):
    """ A socket protocal that facilates two objects communicating with each
        other.

        The only instance methods that should be called in ordinary use are
        'init' and 'main'. Communication should be done through the methods on
        'Client' objects.
    """

    spawn_commands = Dict(Str, Str)

    _port = Int
    _sock = Instance(socket.socket)
    _port_map = Dict(Int, Instance(PortInfo))
    _orphans = List(Instance(PortInfo))
    _pairs = Dict(Instance(PortInfo), Instance(PortInfo))

    # Commands that have been queued for spawned process
    # desired_type -> list of (command, arguments)
    _queue = Dict(Str, List(Tuple(Str, Str)))

    def init(self, pref_path='', pref_node=''):
        """ Read a configuration file and attempt to bind the server to the
            specified port.
        """
        # Bind to port and write port to lock file
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.bind(('localhost', 0))
        self._port = self._sock.getsockname()[1]
        f = open(LOCK_PATH, 'w')
        f.write(str(self._port))
        f.close()

        # Read configuration file
        if not pref_path:
            return
        if os.path.exists(pref_path):
            prefs = Preferences(filename=pref_path)
            if prefs.node_exists(pref_node):
                spawn_node = prefs.node(pref_node)
                for key in spawn_node.keys():
                    cmd = spawn_node.get(key).strip()
                    if cmd.startswith('python '):
                        cmd = cmd.replace('python', sys.executable, 1)
                    self.spawn_commands[key] = cmd
            else:
                msg = "Server could not locate preference node '%s.'"
                logger.error(msg % pref_node)
        else:
            msg = "Server given non-existent preference path '%s'."
            logger.error(msg % pref_path)

    def main(self, port=0):
        """ Starts the server mainloop. If 'port' is specified, the assumption
            is that this Server was spawned from an object on said port. The
            Server will inform the Client that it has been created, and if fails
            to contact the client, this function will return.
        """
        try:
            # Start listening *before* we (potentially) inform the spawner that
            # we are working. This means that if the spawner tries to register,
            # we will be ready.
            logger.info("Server listening on port %i..." % self._port)
            self._sock.listen(5)
            self._sock.settimeout(300)

            # If necessary, inform the launcher that we have initialized
            # correctly by telling it our port
            if port:
                if not send_port(port, "__port__", str(self._port), timeout=5):
                    msg = "Server could not contact spawner. Shutting down..."
                    logger.warning(msg)
                    return

            # Start the mainloop
            while True:
                try:
                    client, address = accept_no_intr(self._sock)
                except socket.timeout:
                    # Every 5 minutes of inactivity, we trigger a garbage
                    # collection. We do this to make sure the server doesn't
                    # stay on, with dead process as zombies.
                    self._gc()
                    continue
                try:
                    if address[0] != '127.0.0.1':
                        msg = "Server received connection from a non-local " \
                            "party (port %s). Ignoring..."
                        logger.warning(msg, address[0])
                        continue
                    command, arguments = receive(client)

                    logger.debug("Server received: %s %s", command, arguments)

                    if command == "send":
                        port, command, arguments = arguments.split(MESSAGE_SEP)
                        self._send_from(int(port), command, arguments)
                    elif command == "register":
                        port, type, other_type = arguments.split(MESSAGE_SEP)
                        self._register(int(port), type, other_type)
                    elif command == "unregister":
                        self._unregister(int(arguments))
                    elif command == "ping":
                        self._send_to(int(arguments), "__status__", "1")
                    elif command == "spawn":
                        self._spawn(arguments)
                    else:
                        logger.error("Server received unknown command: %s %s",
                                     command, arguments)
                finally:
                    client.close()
        finally:
            self._sock.close()

    @staticmethod
    def ping(server_port, timeout=1, error_only=False):
        """ Returns whether the server is running on 'server_port'.

            If error_only, return False only if there was an error (ie the
            socket is closed).
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.bind(('localhost', 0))
        sock.listen(1)
        try:
            port = str(sock.getsockname()[1])
            send_port(server_port, "ping", port, timeout=timeout)
            try:
                server, address = accept_no_intr(sock)
                try:
                    command, arguments = receive(server)
                    return command == "__status__" and bool(int(arguments))
                finally:
                    try:
                        server.shutdown(socket.SHUT_RD)
                    except:
                        pass
            except socket.error:
                # 'sock' may have timed out, so use try..except.
                try:
                    sock.shutdown(socket.SHUT_RD)
                except:
                    pass
                return False
        except:
            try:
                sock.shutdown(socket.SHUT_RD)
            except:
                pass

    def _spawn(self, object_type):
        """ Attempt to spawn an process according the specified type. Returns
            whether this was sucessful.
        """
        try:
            command = self.spawn_commands[object_type]
        except KeyError:
            msg = "No spawn command is defined for object type '%s'." \
                % object_type
            logger.warning(msg)
            return msg

        try:
            logger.info("Server spawning Client of type '%s.'" % object_type)
            spawn_independent(command, shell=True)
        except OSError:
            msg = "Error spawning process for '%s' with command '%s'." \
                % (object_type, command)
            logger.error(msg)
            return msg

        return False

    def _match(self, port):
        """ Attempt to match a registered client on 'port' to another registered
            client of the same type.
        """
        # Try to find a compatible orphan
        info = self._port_map[port]
        for orphan in self._orphans:
            if info.other_type == orphan.type:

                # Ping the orphan to see if its alive:
                if not self._send_to(orphan.port, '__keepalive__', ''):
                    continue

                # Save information about the matching
                self._orphans.remove(orphan)
                self._pairs[info] = orphan
                self._pairs[orphan] = info

                # Dispatch orphaned status to clients
                self._send_to(port, "__orphaned__", "0")
                self._send_to(orphan.port, "__orphaned__", "0")

                # Check command queue and dispatch, if necessary
                for command, arguments in self._queue.pop(info.type, []):
                    self._send_to(port, command, arguments)

                return orphan

        # Otherwise, the object becomes an orphan
        self._orphans.append(info)
        return None

    def _register(self, port, object_type, other_type):
        """ Register a port of 'object_type' that wants to be paired with
            another object of 'other_type'. These types are simply strings.

            Calling 'register' on an already registered port has no effect.
        """
        # Only continue if this object is not already registered
        if port in self._port_map:
            return

        info = PortInfo(port=port, type=object_type, other_type=other_type)
        self._port_map[port] = info
        self._match(port)

    def _unregister(self, port):
        """ Unregister a port. Calling 'unregister' on a port that is not
            registered has no effect.
        """
        try:
            info = self._port_map.pop(port)
        except KeyError:
            return

        if info in self._pairs:
            other = self._pairs.pop(info)
            if other in self._pairs:
                self._pairs.pop(other)
            self._orphans.append(other)
            self._send_to(other.port, "__orphaned__", "1")
        else:
            self._orphans.remove(info)

        # If we have nobody registered, terminate the server.
        if len(self._port_map) == 0:
            logger.info("No registered Clients left. Server shutting down...")
            sys.exit(0)

    def _gc(self):
        """ Garbage collection of the processes. Check that all the orphaned
            processes are still responsive, and if not, unregister them.
        """
        for object_info in self._orphans:
            self._send_to(object_info.port, '__keepalive__', '')
            # _send_to will automatically unregister the port.

    def _send_from(self, port, command, arguments):
        """ Send a command from an object on the specified port.
        """
        try:
            object_info = self._port_map[port]
        except KeyError:
            msg = "Server received a 'send' command from an unregistered " \
                "object (port %s)."
            logger.warning(msg % port)
            return

        try_spawn = False
        if object_info in self._pairs:
            other = self._pairs[object_info]
            while not self._send_to(other.port, command, arguments):
                # The object will automatically be orphaned by _send_to in the
                # event of a communication failure. Try to find another match.
                if object_info in self._orphans:
                    self._orphans.remove(object_info)
                other = self._match(port)
                if other is None:
                    try_spawn = True
                    break
        else:
            try_spawn = True

        if try_spawn:
            queue = self._queue.get(object_info.other_type)
            if queue:
                queue.append((command, arguments))
            else:
                error_msg = self._spawn(object_info.other_type)
                if error_msg:
                    self._send_to(port, '__error__', '1' + error_msg)
                else:
                    self._queue[object_info.other_type] = [(command, arguments)]
                    self._match(port)

    def _send_to(self, port, command, arguments):
        """ Send a command to an object on the specified port. Returns whether
            the command was sent sucessfully.
        """
        status = send_port(port, command, arguments)
        if not status:
            msg = "Server failed to communicate with client on port %i. " \
                "Unregistering..."
            logger.warning(msg % port)
            self._unregister(port)
        return status


def main(pref_path, pref_node, *arg, **kw):
    server = Server()
    server.init(pref_path, pref_node)
    server.main(*arg, **kw)
