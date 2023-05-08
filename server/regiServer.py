from socket import *
import threading
import json

DEBUG=True
MAX_CCU=20

SERVER_VERSION="0.0.1"
SERVER_IP="127.0.0.1"
SERVER_PORT=9998

class Peer:
    def __init__(self, addr, conn, port):
        self.addr=addr
        self.port=port
        self.conn=conn
        
    def __str__(self):
        return str(self.addr[0])+":"+str(self.port)

class Server:
    def __init__(self):
        self.socket=socket(AF_INET, SOCK_STREAM)
        self.peer_list=[None for _ in range(MAX_CCU)]

    def player_thread(self, conn, addr):
        peer=0; crash=False
        while True:
            try:
                if crash: break
                data=self.get_data(conn, 1024)
                res={"qid":0}
                if DEBUG: print("[Client] ", data)
                if data["qid"]==1:
                    res["qid"]=1
                    res["result"]=1
                    for i in range(MAX_CCU):
                        if self.peer_list[i]==None:
                            peer=i
                            self.peer_list[i]=Peer(addr, conn, data["port"])
                            break
                elif data["qid"]==2:
                    addr=[self.peer_list[peer].addr[0], int(self.peer_list[peer].port)]
                    self.peer_list[peer]=None
                    self.broadcast({"qid":2, "addr":addr})
                    crash=True
                    continue
                elif data["qid"]==3:
                    res["qid"]=3
                    online_peers=[]
                    for i in range(MAX_CCU):
                        if self.peer_list[i]!=None and i!=peer:
                            online_peers.append(str(self.peer_list[i]))
                    res["result"]=len(online_peers)
                    res["peers"]=online_peers

                self.send_data(conn, res)
            except Exception as e:
                print("[ERROR_player_thread]", e)
                try: 
                    self.send_data(conn, {"qid":0})
                except:
                    addr=[self.peer_list[peer].addr[0], int(self.peer_list[peer].port)]
                    self.peer_list[peer]=None
                    self.broadcast({"qid":2, "addr":addr})
                    crash=True


    def send_data(self, client, msg):
        if DEBUG: print("[SERVER] ", msg)
        client.send(json.dumps(msg).encode())

    def broadcast(self, msg):
        for i in range(MAX_CCU):
            if self.peer_list[i]==None: continue
            self.send_data(self.peer_list[i].conn, msg)
    
    def get_data(self, conn, bytes):
        data=conn.recv(bytes)
        data=json.loads(data.decode())
        return data

    def connect(self):
        try:
            self.socket.bind((SERVER_IP, SERVER_PORT))
        except: pass

        while True:
            try:
                self.socket.listen()
                conn, addr=self.socket.accept()
                pthread=threading.Thread(target=self.player_thread, args=(conn, addr))
                pthread.start()
            except Exception as e: 
                print(e)


server=Server()
thread=threading.Thread(target=server.connect)
thread.start()
print("SERVER START")