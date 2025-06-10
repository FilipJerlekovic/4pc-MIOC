from winsound import *

def onMove():
    return PlaySound('.\\Sounds\\move.wav', SND_ASYNC)

def onTake():
    return PlaySound('.\\Sounds\\take.wav', SND_ASYNC)

def onCastle():
    return PlaySound('.\\Sounds\\castle.wav', SND_ASYNC)

def onCheckmate():
    return PlaySound('.\\Sounds\\boom.wav', SND_ASYNC)

def onCheck():
    return PlaySound('.\\Sounds\\check.wav', SND_ASYNC)

def onPromo():
    return PlaySound('.\\Sounds\\hrt.wav', SND_ASYNC)

def win():
    return PlaySound('.\\Sounds\\win.wav', SND_ASYNC)


if __name__ == "__main__":
    onCheckmate()