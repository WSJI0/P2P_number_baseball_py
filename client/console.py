def cprint(msg, color='white', end='\n'):
    colors={
        'white':37,
        'red':91,
        'blue':94,
        'green':32,
        'cyan':96,
        'yellow':33
    }
    print("\033["+str(colors[color])+"m"+msg+"\033[0m", end=end, flush=True)

def printHelp():
    cprint("========================================", "yellow")
    cprint("help :", "blue", ''); print(" available commands")
    cprint("logoff :", "blue", ''); print(" logoff and quit program")
    cprint("connect [peer] :", "blue", ''); print(" start game with selected peer")
    cprint("disconnect [peer] [peer] ... :", "blue", ''); print(" end game with selected peers")
    cprint("list :", "blue", ''); print(" list of online peers")
    cprint("conn :", "blue", ''); print(" list of connected peers")
    cprint("guess [peer] [your guessing number] :", "blue", ''); print(" guessing number of selected peer")
    cprint("block [peer] :", "blue", ''); print(" block selected peer")
    cprint("========================================", "yellow")


class Console:
    def __init__(self, peer):
        self.peer=peer
        self.command=""
        self.history=""
        self.peer.reg_console(self)

    def userCLI(self):
        import msvcrt as getch

        while True:
            try:
                c=getch.getch().decode("utf-8")
                if c!='\r': 
                    if c=='\b':
                        self.command=self.command[:-1]
                        print('\r'+' '*100, end='\r')
                        cprint(self.command, "yellow", '')
                    else: 
                        self.command+=c
                        cprint(c, "yellow", '')
                    continue
            except: pass
            print()
            try:
                commands=self.command.split()
                self.history=self.command
                self.command=""
                if commands[0]=="logoff":
                    self.peer.logout()
                    break
                elif commands[0]=="help":
                    printHelp()
                elif commands[0]=="connect":
                    self.peer.connect(commands[1])
                elif commands[0]=="disconnect":
                    self.peer.disconnect(commands[1:])
                elif commands[0]=="list":
                    self.peer.get_peer_list()
                elif commands[0]=="guess":
                    self.peer.guess(commands[1], commands[2]+" "+commands[3]+" "+commands[4])
                elif commands[0]=="conn":
                    self.peer.print_connected_list()
                elif commands[0]=="block":
                    self.peer.block(commands[1])
                else:
                    cprint("wrong command", "red")
            except:
                cprint("wrong command", "red")
                self.command=""

    def printQ(self, msg):
        print('\r'+' '*100, end='\r')
        print(msg)
        cprint(self.command, "yellow", '')