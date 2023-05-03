import json
import threading
from socket import *
from game import Game

SERVER_IP="25.11.91.11"
SERVER_PORT=9998
DEBUG=True

class Network:
    def __init__(self, ip=SERVER_IP, port=SERVER_PORT):
        self.socket=socket(AF_INET, SOCK_STREAM)
        self.socket.connect((ip, port))
        self.lobby=None
        self.game=None
        self.peer=None
        self.send_data({"qid":1})    

    def join_peer(self, peer):
        self.peer=peer

    def send_data(self, msg):
        self.socket.send(json.dumps(msg).encode())

    def logout(self):
        self.send_data({"qid":2})
        self.socket.close()

    def get_peer_list(self):
        self.send_data({"qid":3})

    def startGame(self):
        self.send_data({"qid":4})

    def guess(self, number):
        self.send_data({"qid":5, "guess":number})

    def get_data(self):
        rec=[]; res=None
        while True:
            try:
                rec.append(self.socket.recv(1024))
                data=json.loads(rec.pop().decode())
                if DEBUG: print("GET:", data)

                if data["qid"]==0:
                    print("error")
                elif data["qid"]==1:
                    print("login success")
                elif data["qid"]>=3:
                    res=self.peer.process(data)
                
                if res!=None:
                    self.send_data({"qid":6, "answer":res})
            except Exception as e:
                # self.socket.close()
                print("[Network ERROR]", e)

    def connect(self):
        try:
            self.socket.bind((SERVER_IP, SERVER_PORT))
        except: pass

        while True:
            try:
                self.socket.listen()
                conn, addr=self.socket.accept()
                pthread=threading.Thread(target=self.get_data, args=(conn, addr))
                pthread.start()
                self.peer.add_peer(self)
            except Exception as e: 
                print(e)