import socket
import time

from sources import FileSource

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    source = FileSource(1, s)
    source_stream = source.get_stream(None)
    while source_stream.is_active():
        time.sleep(0.1)
    source.close()