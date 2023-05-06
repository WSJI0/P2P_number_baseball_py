import threading
from network import NetworkTCP, NetworkUDP
from game import Game

SERVER_IP="127.0.0.1"
SERVER_PORT=9998
CLIENT_IP="127.0.0.1"
CLIENT_PORT=9999

class Peer:
    def __init__(self, port):
        global CLIENT_PORT

        self.game=Game()
        self.game.initGame()

        CLIENT_PORT=int(port)

        self.regiServer=NetworkTCP(SERVER_IP, SERVER_PORT, CLIENT_PORT)  # regiServer랑 연결
        self.peerServer=NetworkUDP(CLIENT_IP, CLIENT_PORT, CLIENT_PORT, True)  # 다른 peer들과의 연결
        self.online_peers=[] # 현재 online인 peer들의 ip
        self.connected_peers=[]  # 연결된 peer들의 ip (현재 게임중인 peer들)
        self.black_list=[] # 블랙리스트
        self.console=None

        self.regiServer.join_peer(self)
        self.peerServer.join_peer(self)
        
        self.server_thread=threading.Thread(target=self.regiServer.get_data)
        self.server_thread.daemon=True
        self.server_thread.start()

        self.peer_thread=threading.Thread(target=self.peerServer.get_data)
        self.peer_thread.daemon=True
        self.peer_thread.start()

    def reg_console(self, console):
        self.console=console

    def logout(self):
        self.regiServer.logout()

    def block(self, peer):
        self.console.printQ(str(self.online_peers[int(peer)-1])+" has been blacklisted.")
        b=self.online_peers[int(peer)-1].split(':')
        self.black_list.append([b[0], int(b[1])])
        self.online_peers.pop(int(peer)-1)

    def connect(self, number):
        if int(number)>len(self.online_peers): return
        if self.add_peer(self.online_peers[int(number)-1]):
            self.network(len(self.connected_peers)).startGame()
            self.console.printQ("start game with peer"+str(number))

    def disconnect(self, peers):
        for i in peers:
            i=int(i)-1
            self.network(int(i)).disconnect()
            self.pop_peer(self.connected_peers[int(i)])

    def crashed(self, addr):
        if addr not in self.connected_peers: return
        self.console.printQ(str(addr[0])+":"+str(addr[1])+" disconnected")
        self.pop_peer(addr)
    
    def get_peer_list(self):
        self.regiServer.get_peer_list()

    def print_connected_list(self):
        if len(self.connected_peers)==0:
            self.console.printQ("No connections")
            return

        self.console.printQ("==== Connected peers ====")
        for i in range(len(self.connected_peers)):
            self.console.printQ("["+str(i+1)+"] "+str(self.connected_peers[i][0])+":"+str(self.connected_peers[i][1]))

    def add_peer(self, peer):
        p=peer.split(':')
        if [p[0], int(p[1])] not in self.connected_peers:
            self.connected_peers.append([p[0], int(p[1])])
            return True
        return False

    def pop_peer(self, addr):
        for i in range(len(self.connected_peers)):
            if self.connected_peers[i]==addr:
                self.connected_peers.pop(i)
                break

    def network(self, peer):
        p=self.connected_peers[int(peer)-1]
        return NetworkUDP(p[0], p[1], CLIENT_PORT, False)

    def guess(self, peer, number):
        self.network(int(peer)).guess(number)

    def get_answer(self, number):
        return self.game.answer(number)

    def process(self, data):
        if data["qid"]==3:
            self.console.printQ("=== Online peer list ===")
            self.console.printQ("[You] "+str(CLIENT_IP)+":"+str(CLIENT_PORT))
            if data["result"]==0:
                self.console.printQ("Thre is no other online peers ..")
            else:
                self.online_peers=[]
                for i in range(int(data["result"])):
                    try:
                        d_tmp=data["peers"][i].split(':')
                        if [d_tmp[0], int(d_tmp[1])] not in self.black_list:
                            self.online_peers.append(data["peers"][i])
                    except: pass
                for i in range(len(self.online_peers)):
                    self.console.printQ("["+str(i+1)+"] "+str(self.online_peers[i]))
        elif data["qid"]==4:
            d_tmp=data["addr"].split(':')
            if [d_tmp[0], int(d_tmp[1])] not in self.black_list:
                self.console.printQ("new peer connected. ")
                self.add_peer(data["addr"])
        elif data["qid"]==5:
            strike, ball=self.get_answer(data["guess"])
            return [strike, ball]
        elif data["qid"]==6:
            if data["answer"][0]==-1:
                self.console.printQ("wrong input")
            else:
                self.console.printQ(str(data["answer"][0])+" Strike   "+str(data["answer"][1])+" Ball")
        elif data["qid"]==7:
            self.console.printQ("peer disconnected..")
            self.pop_peer(data["addr"])

        return None