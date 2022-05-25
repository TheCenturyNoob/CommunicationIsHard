import socket
import time

from sources import FileSource
from targets import Target

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

target = Target(4, 2, 48000)
target_stream = target.get_stream()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print('listening')
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(6144)
            if not data:
                print('breaking')
                break
            else:
                # print(data)
                target_stream.write(data)