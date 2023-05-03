def printC(msg, color='white', end='\n'):
    colors={
        'white':37,
        'red':91,
        'blue':94,
        'green':32,
        'cyan':96,
        'yellow':33
    }
    print("\033["+str(colors[color])+"m"+msg+"\033[97m", end=end)