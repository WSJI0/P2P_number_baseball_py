import threading
from game import Game
from peer import Peer
from color import printC

def printHelp():
    printC("========================================", "yellow")
    printC("help :", "blue", ''); print(" available commands")
    printC("logoff :", "blue", ''); print(" logoff and quit program")
    printC("start :", "blue", ''); print(" start game with online peers")
    printC("disconnect [peer] :", "blue", ''); print(" end game with selected peer")
    printC("guess [peer] [your guessing number] :", "blue", ''); print(" guessing number of selected peer")
    printC("========================================", "yellow")


def userCLI():
    while True:
        command=input(">")
        if command=="logoff":
            peer.logout()
            break
        elif command=="help":
            printHelp()
        elif command=="start":
            peer.get_peer_list()
        elif command=="guess":
            arg=input().split()
            peer.guess(arg[0], arg[1])

peer=Peer()
player_thread=threading.Thread(target=userCLI)
player_thread.start()