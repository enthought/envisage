# Standard library imports
import os, sys
import socket
from subprocess import Popen

# ETS imports
from enthought.etsconfig.api import ETSConfig

# An obscure ASCII character that we used as separators in socket streams
MESSAGE_SEP = chr(7) # 'bell' character

# The location of the server lock file and the communication log
LOCK_PATH = os.path.join(ETSConfig.application_data, 'enshell_server.lock')
LOG_PATH = os.path.join(ETSConfig.application_data, 'enshell_server.log')


def spawn_independent(command, shell=False):
    """ Given a command suitable for 'Popen', open the process such that when
        this process is killed, the spawned process survives.
    """
    if sys.platform == 'win32':
        Popen(command, shell=shell)
    else:
        pid = os.fork()
        if pid:
            return
        else:
            os.setpgrp()
            Popen(command, shell=shell)
            sys.exit(0)


def get_server_port():
    """ Reads the server port from the lock file. If the file does not exist
        returns -1.
    """
    if os.path.exists(LOCK_PATH):
        f = open(LOCK_PATH, 'r')
        try:
            return int(f.read().strip())
        finally:
            f.close()
    else:
        return -1


def send(sock, command, arguments=''):
    """ Send a command with arguments (both strings) through a socket. This
        information is encoded with length information to ensure that
        everything is recieved.        
    """
    sent, total = 0, 0
    msg = command + MESSAGE_SEP + arguments
    msg = str(len(msg)) + MESSAGE_SEP + msg
    length = len(msg)
    while total < length:
        msg = msg[sent:]
        sent = sock.send(msg)
        if not sent:
            print "raised by Me"
            raise socket.error
        total += sent


def send_port(port, command, arguments='', timeout=None):
    """ A send a command to a port. Convenience function that uses 'send'.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if timeout is not None:
        sock.settimeout(timeout)
    errno = sock.connect_ex(('localhost', port))
    if errno:
        sock.close()
        return False
    
    try:
        send(sock, command, arguments)
    except socket.error:
        return False
    finally:
        sock.shutdown(socket.SHUT_WR)
        
    return True


def recieve(sock):
    """ Recieve a command with arguments from a socket that was previously
        sent information with 'send'.
    """
    index = -1
    chunk, length = '', ''
    while index == -1:
        length += chunk
        chunk = sock.recv(4096)
        if not chunk:
            raise socket.error
        index = chunk.find(MESSAGE_SEP)
    length = int(length + chunk[:index])

    msg = chunk[index+1:]
    while len(msg) < length:
        chunk = sock.recv(length - len(msg))
        if not chunk:
            raise socket.error
        msg += chunk

    command, sep, arguments = msg.partition(MESSAGE_SEP)
    return command, arguments
