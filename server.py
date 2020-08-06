# -*- coding: utf-8 -*-

import json
import socket
import select

from config import Config


class Server:
    def __init__(self):
        fd = open("config.json")
        config = json.load(fd)

        self.config = Config(**config)

        self.connections = {}
        self.addresses = {}

        self.init()

    def init(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind()
        self.set_sockopt()

        self.epoll = select.epoll()
        self.epoll.register(self.s.fileno(), select.EPOLLIN | select.EPOLLET)

    def bind(self):
        self.s.bind((self.config.bind, self.config.port))
        self.s.listen(self.config.listen)

    def set_sockopt(self):
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        print("server start at {} bind to {}...".format(self.config.port, self.config.bind))
        while True:
            eplist = self.epoll.poll()
            for fd, event in eplist:
                if fd == self.s.fileno():
                    self.new_connection_come()
                else:
                    self.deal_with_data(fd, event)

    def deal_with_data(self, fd, event):
        if event & select.EPOLLIN:
            self.deal_with_data_in(fd, event)
        elif event & select.EPOLLOUT:
            self.deal_with_data_out(fd, event)
        elif event & select.EPOLLHUP:
            self.deal_with_event_hup(fd, event)

    def deal_with_data_in(self, fd, event):
        recv_data = self.connections[fd].recv(1024)
        print("read data from peer: {}".format(recv_data))
        self.epoll.modify(fd, select.EPOLLOUT)

    def deal_with_data_out(self, fd, event):
        data = b"hello"
        self.connections[fd].send(data)
        self.epoll.modify(fd, select.EPOLLHUP)

    def deal_with_event_hup(self, fd, event):
        self.epoll.unregister(fd)
        self.connections[fd].close()
        del self.connections[fd]

    def new_connection_come(self):
        conn, addr = self.s.accept()
        print("new connection from addr ip: {}, port: {}".format(addr[0], addr[1]))
        self.connections[conn.fileno()] = conn
        self.addresses[conn.fileno()] = addr
        self.epoll.register(conn.fileno(), select.EPOLLIN | select.EPOLLET)


if __name__ == '__main__':
    Server().run()
