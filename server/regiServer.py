from socket import *
import threading
import json

DEBUG=True
MAX_CCU=20

SERVER_VERSION="0.0.1"
SERVER_IP="25.11.91.11"
SERVER_PORT=9998

class Peer:
    def __init__(self, addr, conn):
        self.addr=addr
        self.conn=conn
        
    def __str__(self):
        return str(self.addr[0])+":"+str(self.addr[1])

class Server:
    def __init__(self):
        # TCP
        self.socket=socket(AF_INET, SOCK_STREAM)
        self.peer_list=[None for _ in range(MAX_CCU)]

    def player_thread(self, conn, addr):
        peer=0
        while True:
            try:
                data=self.get_data(conn, 1024)
                res={"qid":0}
                if DEBUG: print("[Client] ", data)
                if data["qid"]==1:
                    res["qid"]=1
                    res["result"]=1
                    for i in range(MAX_CCU):
                        if self.peer_list[i]==None:
                            peer=i
                            self.peer_list[i]=Peer(addr, conn)
                            break
                elif data["qid"]==2:
                    self.peer_list[peer]=None
                    continue
                elif data["qid"]==3:
                    res["qid"]=3
                    online_peers=[]
                    for i in range(MAX_CCU):
                        if self.peer_list[i]!=None and i!=peer:
                            online_peers.append(str(self.peer_list[i]))
                    res["result"]=len(online_peers)
                    res["peers"]=online_peers
                elif data["qid"]==5:
                    pass

                self.send_data(conn, res)
            except Exception as e:
                try: self.send_data(conn, {"qid":0})
                except: pass
                self.peer_list[peer]=None
                print("[ERROR_player_thread]", e)
                break


    def send_data(self, client, msg):
        if DEBUG: print("[SERVER] ", msg)
        client.send(json.dumps(msg).encode())

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