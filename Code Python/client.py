import socket 
import json


class Client:
    header_size = 10

    def __init__(self, host, port, username):
        self.client = self.initial_client(host, port)        
        self.username = username

    @staticmethod
    def initial_client(host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        return client

    def make_msg(self, data_type="hello", data="Hello Server"):
        dic = {"type": data_type, "content": data}
        return dic

    def _encode(self, msg, data_type="hello"):
        dic = self.make_msg(data_type=data_type, data=msg)
        encoded_msg = json.dumps(dic).encode("utf-8")
        header = f"{len(encoded_msg)}"
        while len(header) < self.header_size:
            header += ' '
        return header.encode('utf-8') + encoded_msg

    def recv(self):
        header = self.client.recv(self.header_size).decode("utf-8")
        len_msg = int(header)
        encoded_msg = self.client.recv(len_msg).decode("utf-8")
        msg = json.loads(encoded_msg)
        return msg

    def send(self, msg, data_type="hello"):
        encoded_msg = self._encode(msg, data_type=data_type)
        self.client.send(encoded_msg)
        response = self.recv()
        return response


if __name__ == "__main__":
    host = socket.gethostname()
    port = 1234
    #host = "3.22.53.161"
    #port = 11020
    client = Client(host, port, "Thao")
    msg = client.recv()
    print(msg)
    client.client.send(client._encode("Hello Server"))
    #msg = client.send(client.make_msg())
        

