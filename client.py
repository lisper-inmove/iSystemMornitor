# -*- coding: utf-8 -*-


import socket
import json

if "__main__" == __name__:
    for x in range(1, 2):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        sock.connect(('127.0.0.1', 33191));
        data = [[1, 1002, "2015-01-01", "192.168.10.219", "this is a test"]]
        sock.send(json.dumps(data).encode("utf8"));

        sock.close();
    print("end of connect");
