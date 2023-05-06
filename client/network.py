import json
import threading
from socket import *
from game import Game


DEBUG=False

class NetworkTCP:
    def __init__(self, ip, port, cl_port):
        self.socket=socket(AF_INET, SOCK_STREAM)
        self.peer=None
        self.socket.connect((ip, port))
        self.send_data({"qid":1, "port":cl_port})
        self.crash=False

    def join_peer(self, peer):
        self.peer=peer

    def send_data(self, msg):
        self.socket.send(json.dumps(msg).encode())

    def logout(self):
        self.send_data({"qid":2})
        self.crash=True
        self.socket.close()

    def get_peer_list(self):
        self.send_data({"qid":3})

    def get_data(self):
        while True:
            if self.crash: break
            try:
                data=json.loads(self.socket.recv(1024).decode())
                if DEBUG: print("[SERVER] ", data)

                if data["qid"]==0:
                    print("error")
                    break
                elif data["qid"]==1:
                    print("login success")
                elif data["qid"]==2:
                    self.peer.crashed(data["addr"])
                elif data["qid"]>=3:
                    self.peer.process(data)
            except Exception as e:
                print("[Network ERROR]", e)

class NetworkUDP:
    def __init__(self, ip, port, my_port, host):
        self.ip=ip
        self.port=port
        self.my_port=my_port
        self.socket=socket(AF_INET, SOCK_DGRAM)
        self.peer=None
        if host:
            try:
                self.socket.bind((ip, port))
            except: pass

    def join_peer(self, peer):
        self.peer=peer

    def send_data(self, msg):
        self.socket.sendto(json.dumps(msg).encode(), (self.ip, self.port))

    def startGame(self):
        self.send_data({"qid":4, "port":self.my_port})

    def guess(self, number):
        self.send_data({"qid":5, "guess":number, "port":self.my_port})

    def disconnect(self):
        self.send_data({"qid":7, "port":self.my_port})

    def get_data(self):
        rec=[]; res=None
        while True:
            try:
                msg, addr=self.socket.recvfrom(1024)
                data=json.loads(msg.decode())

                if data["qid"]==0:
                    # print("error")
                    continue
                elif data["qid"]==4:
                    data["addr"]=addr[0]+":"+str(data["port"])
                    self.peer.process(data)
                elif data["qid"]==5:
                    strike, ball=self.peer.process(data)
                    NetworkUDP(addr[0], int(data["port"]), self.my_port, False).send_data({"qid":6, "answer":[strike, ball]})
                elif data["qid"]==6:
                    self.peer.process(data)
                elif data["qid"]==7:
                    data["addr"]=[addr[0], data["port"]]
                    self.peer.process(data)
                
            except Exception as e:
                # self.socket.close()
                if DEBUG: print("[Network ERROR]", e)