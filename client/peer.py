import threading
import sys
from network import Network
from game import Game

class Peer:
    def __init__(self):
        self.regiServer=Network()
        self.connected_peers=[]
        self.game=None
        self.regiServer.join_peer(self)
        
        self.server_thread=threading.Thread(target=self.regiServer.get_data)
        self.server_thread.daemon=True
        self.server_thread.start()

    def logout(self):
        self.regiServer.logout()
    
    def get_peer_list(self):
        self.game=Game()
        self.game.initGame()
        self.regiServer.get_peer_list()

    def add_peer(self, peer):
        self.connected_peers.append(peer)
        conn_thread=threading.Thread(target=self.peer.connect)
        conn_thread.daemon=True
        conn_thread.start()

    def guess(self, peer, number):
        self.connected_peers[peer-1].guess(number)

    def get_answer(self, number):
        self.game.answer(number)

    def process(self, data):
        if data["qid"]==3:
            if data["result"]==0:
                print("Thre is no other online peers")
            else:
                print("Game will start soon..")
                offline_peers=[]
                for i in range(int(data["result"])):
                    try:
                        p=Network(data["peers"][0], data["peers"][1])
                        self.add_peer(p)
                        self.connected_peers[-1].startGame()
                    except:
                        offline_peers.append(i)
                # sys("cls")
                print("game started with "+str(len(self.connected_peers))+" players")
        elif data["qid"]==4:
            print("new peer connected. ")
        elif data["qid"]==5:
            strike, ball=self.get_answer(data["number"])
            return [strike, ball]
        elif data["qid"]==6:
            if data["answer"][0]==-1:
                print("wrong input")
            else:
                print(str(data["answer"][0])+" Strike   "+str(data["answer"][1])+" Ball")
        
        return None