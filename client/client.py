import sys
import threading
import colorama
from game import Game
from peer import Peer
from console import Console

colorama.init()

port=9999
if len(sys.argv)==2:
    port=sys.argv[1]

console=Console(Peer(port))
player_thread=threading.Thread(target=console.userCLI)
player_thread.start()