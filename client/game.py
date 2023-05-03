class Game:
    def __init__(self):
        self.number=[0, 0, 0]

    def setNumber(self, inp):
        inp=inp.split()

        if len(inp)!=3: return False
        for i in range(3):
            if inp[i]>'9' or inp[i]<'0': return False
            inp[i]=int(inp[i])
        if inp[0]==inp[1] or inp[0]==inp[2] or inp[1]==inp[2]: return False
        
        for i in range(3): 
            self.number[i]=inp[i]
        return True
    
    def checkValidInput(self, inp):
        inp=inp.split()
        if len(inp)!=3: return False
        for i in range(3):
            if inp[i]>'9' or inp[i]<'0': return False
        return True
    
    def answer(self, inp):
        strike=0; ball=0
        if not self.checkValidInput(inp):
            return -1, -1
        
        inp=list(map(int, inp.split()))
        for i in range(3):
            if inp[i]==self.number[i]:
                strike+=1
        for i in range(3):
            for j in range(3):
                if i==j: continue
                if inp[i]==self.number[j]:
                    ball+=1
        
        return strike, ball

    def initGame(self):
        inp=""
        while inp=="":
            inp=input("your number(x x x) : ")
            if not self.setNumber(inp):
                inp=""