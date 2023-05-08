import json
import time
from socket import *

DEBUG=False

class NetworkTCP:
    def __init__(self, ip, port, cl_port):
        self.socket=None
        self.peer=None
        self.ip=ip
        self.port=port
        self.cl_port=cl_port
        self.connected=False
        self.init_connection=True

        self.connect()

    def connect(self, msg=True):
        try:
            self.socket=socket(AF_INET, SOCK_STREAM)
            self.socket.connect((self.ip, self.port))
            self.connected=True
            # print("server connected")
        except:
            if msg:
                self.peer.console.printQ("[ Server offline ] Please try again..")
            self.connected=False

        if self.connected:
            self.send_data({"qid":1, "port":self.cl_port})

    def join_peer(self, peer):
        self.peer=peer

    def send_data(self, msg):
        try:
            self.socket.send(json.dumps(msg).encode())
        except: 
            self.connected=False

    def logout(self):
        self.send_data({"qid":2})
        self.crash=True
        self.socket.close()

    def get_peer_list(self):
        if not self.connected:
            self.peer.console.printQ("Trying to reconnect..")
            self.connect()
        self.send_data({"qid":3})

    def get_data(self):
        while True:
            if not self.connected: 
                self.connect(False)
                time.sleep(3)
                continue
            try:
                data=json.loads(self.socket.recv(1024).decode())
                if DEBUG: print("[SERVER] ", data)

                if data["qid"]==0:
                    pass
                    # print("error")
                    # break
                elif data["qid"]==1:
                    if self.init_connection:
                        self.init_connection=False
                        print("login success")
                elif data["qid"]==2:
                    self.peer.crashed(data["addr"])
                elif data["qid"]>=3:
                    self.peer.process(data)
            except Exception as e:
                if self.connected:
                    self.socket.close()
                    self.connected=False
                # print("[Network ERROR]", e)

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