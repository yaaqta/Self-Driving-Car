import socket 
from time import time
from get_image import convert_csv_to_image
from select import select
import pickle
import json
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


class Server:
    header_size = 10

    def __init__(self, host, port):
        self.server = self.initialize_server(host, port)
        self.server.listen()
        self.sockets = [self.server]
        self.image = None
        self.binary_image = None
        self.addr = {}

    @staticmethod
    def initialize_server(host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        return server

    def _encode(self, msg):
        msg = json.dumps(msg)
        encode_msg = msg.encode('utf-8')
        header = f"{len(encode_msg)}"
        while len(header) < self.header_size:
            header += ' '
        return header.encode('utf-8') + encode_msg

    def send(self, conn, msg):
        encode_msg = self._encode(msg)
        conn.send(encode_msg)

    def recv(self, conn):
        header_msg = conn.recv(self.header_size)
        size = int(header_msg.decode('utf-8'))
        msg = conn.recv(size) 
        decode_msg = json.loads(msg.decode('utf-8'))
        return decode_msg

    @staticmethod
    def get_dictionary(data_type="image", data=[[2, 3, 4], [1, 2, 3]]):
        dic = {}
        dic["type"] = data_type
        dic["content"] = data
        return dic

    def run(self):
        print("[RUNNING] Server is running ...")

        while True:
            readable, _, _ = select(self.sockets, [], self.sockets)
            for socket in readable:
                if socket == self.server:
                    conn, addr = self.server.accept()
                    self.addr[conn] = addr
                    print(f"[CONNECT] {addr[0]}:{addr[1]} connected.")
                    self.sockets.append(conn)
                    #self.send(conn, self.get_dictionary(data_type="hello", data="Hello Guys"))
                else:
                    try:
                        msg = self.recv(socket)
                        if msg["type"] == "hello":
                            print(f"[RECEIVE] Receive a greeting from {self.addr[socket][0]}:{self.addr[socket][1]}") 
                            print(msg)
                        elif msg["type"] == "image":
                            print(f"[RECEIVE] Receive an image from {self.addr[socket][0]}:{self.addr[socket][1]}") 
                            self.image = msg['content']
                            self.send(socket, self.get_dictionary(data_type="receive", data="Server is reiceived."))
                        elif msg["type"] == "binary_img":
                            print(f"[RECEIVE] Receive a binary image from {self.addr[socket][0]}:{self.addr[socket][1]}") 
                            self.binary_image = msg['content']
                            self.send(socket, self.get_dictionary(data_type="receive", data="Server is reiceived."))
                        elif msg["type"] == "get_image":
                            print(f"[SEND] Send an image to {self.addr[socket][0]}:{self.addr[socket][1]}")
                            self.send(socket, self.get_dictionary(data_type="send_image", data=self.image))
                        elif msg["type"] == "get_binary_image":
                            print(f"[SEND] Send a binary image to {self.addr[socket][0]}:{self.addr[socket][1]}")
                            self.send(socket, self.get_dictionary(data_type="send_image", data=self.binary_image))
                        elif  msg["type"] == "run":
                            first = time()
                            convert_csv_to_image("labview\\data.csv")
                            print(f"[CONVERT] convert to image in {time() - first}")


                    except Exception as e:
                            print(f"[ERROR] {e}") 
                            self.sockets.remove(socket)
                            del self.addr[socket]

                    break 
                break


if __name__ == "__main__":
    host = ""
    port = 1234
    Server(host, port).run()


