from tkinter import *
from tkinter import font
import copy
import explosion
import SoundHandler
import win

from simulator import Chess, Piece


game = Chess()
game.setupBoard()

prozor = Tk()
DISPLAY_WIDTH = prozor.winfo_screenwidth()
DISPLAY_HEIGHT = prozor.winfo_screenheight()
prozor.after(1, lambda: prozor.focus_force())
prozor.geometry(f"850x800+{(DISPLAY_WIDTH-850)//2}+{(DISPLAY_HEIGHT-800)//2}")
global_font=("Courier New", 5)
prozor.option_add("*Font", global_font)

WHITE = "#cbd6ce"
BLACK = "#7d7d7d"
WHITESELECT = "#a6a283"
BLACKSELECT = "#595741"

GLOBAL_DEBUG = True
DEBUG_PIECE_CREATION = 1



boardButtonNames = [] # modern problems require not so modern solutions

# trackaj turn
turnLabel = Label(prozor, text=("TURN " + "RGYB"[game.turn]), font=("Courier New", 10))
turnLabel.grid(row=20, column = 19)

#sada je veličina jednog height i width 14 px, hvala bogu da se nekako potrefilo

sigmar = []
for i in range(14):
    gooner = []
    for j in range(14):
        gooner.append('.')
    sigmar.append(gooner)

SHIFT_DOWN = False
def colorSwitch(primary1, primary2, secondary1, secondary2, check):
    if check == primary1: return secondary1
    elif check == primary2: return secondary2
    else: return check # nista


    
# DEBUG METODE
def genocid(event): # ubi na LMB
    global game, sigmar, boardButtonNames, imageCache
    if str(type(event.widget)) != "<class 'tkinter.Button'>": return -1 # ne valja
    if (str(event.widget) not in boardButtonNames): return -1
    data = event.widget.grid_info()
    column = data["column"]
    row = data["row"]
    piece = game.get(column, row)
    piece.type = 0
    piece.color = -1
    sigmar[column][row].config(image = "", width = 1, height = 1)


def genesis(event): # stvori pijuna trenutnog igraca na MMB
    print("a")
    global game, sigmar, boardButtonNames, imageCache, DEBUG_PIECE_CREATION
    print(str(type(event.widget)))
    if str(type(event.widget)) != "<class 'tkinter.Button'>": return -1 # ne valja
    print("aa")
    if (str(event.widget) not in boardButtonNames): return -1
    print("aaa")
    data = event.widget.grid_info()
    column = data["column"]
    row = data["row"]
    piece = game.get(column, row)
    piece.type = DEBUG_PIECE_CREATION
    piece.color = game.turn
    print(piece)
    sigmar[column][row].config(image = imageCache[str(piece)], width = 8, height = 8)
    prozor.update()

def geneza(event):
    global DEBUG_PIECE_CREATION
    DEBUG_PIECE_CREATION = max(1, (DEBUG_PIECE_CREATION + 1) % 7)

def deebug(event):
    global game
    data = event.widget.grid_info()
    column = data["column"]
    row = data["row"]
    print(column, row)
    game.debug()



def destroyPiece(piece):
    global game, sigmar, prozor
    piece.type, piece.color = 0, -1
    sigmar[piece.x][piece.y].config(image = "", height = 1, width = 1) # krađa identiteta
    prozor.update()

def goyim(event):
    # TODO: dodaj način da detektiraš jesi li stisnuo na ploču ili van na druge gumbe ak ih ikada implementiram
    global game, sigmar, boardButtonNames, imageCache
    # print(type(event.widget))
    # print(event.widget)
    if str(type(event.widget)) != "<class 'tkinter.Button'>": return -1 # ne valja
    if (str(event.widget) not in boardButtonNames): return -1
    # print("bleh")
    data = event.widget.grid_info()
    column = data["column"]
    row = data["row"]
    # get associated Chess.board element
    piece = game.get(column, row)
    # print(piece)
    attempt = tkMove(piece)
    # game.debug()
    # print(game.turn)
    
    if attempt:
        actionType = None
        raceGuesser = attempt[1].type
        # print("a")
        # castling check
        # ("ATT: ", attempt[0], attempt[1])
        if attempt[0].color == attempt[1].color and attempt[0].type == 6 and attempt[1].type == 2: # castle check
            # print("bombardiro corooridlo")
            # print(attempt[0], attempt[0].moved)
            # print(attempt[1], attempt[1].moved)
            if not (attempt[0].moved or attempt[1].moved): # move check
                # print("tralalellotllarlarlalral")
                # blank check
                flag = True
                if attempt[0].color in [0, 2]:
                    # blank check
                    for i in range(min(attempt[0].x, attempt[1].x) + 1, max(attempt[0].x, attempt[1].x)):
                        if game.get(i, attempt[0].y).type != 0:
                            flag = False
                            break
                    
                    # gavrilo princip check
                    for i in range(min(attempt[0].x, attempt[1].x), max(attempt[0].x, attempt[1].x)):
                        if i == attempt[1].x: continue
                        if game.checkAttacked(game.get(i, attempt[0].y)):
                            flag = False
                            break
                else:
                    for i in range(min(attempt[0].y, attempt[1].y) + 1, max(attempt[0].y, attempt[1].y) - 1):
                        if game.get(attempt[0].x, i).type != 0 :
                            flag = False
                            break

                    for i in range(min(attempt[0].y, attempt[1].y), max(attempt[0].y, attempt[1].y)):
                        if i == attempt[1].y: continue
                        if game.checkAttacked(game.get(attempt[0].x, i)):
                            flag = False
                            break
                
                if flag:
                    # print("JAJAJAJJA")
                    SoundHandler.onCastle()
                    # switchaj 
                    kingPos, rookPos = None, None
                    if attempt[0].color in [0,2]:
                        kingPos = (attempt[0].x + attempt[1].x) // 2
                        rookPos = kingPos
                        if attempt[0].x < attempt[1].x: kingPos += 1
                        else: rookPos += 1
                        # print("################", kingPos, rookPos)
                        king = str(attempt[0])
                        rook = str(attempt[1])
                        kingTarget = game.get(kingPos, attempt[0].y)
                        rookTarget = game.get(kingPos, attempt[0].y)
                        # resetiraj prethodne pozicije
                        sigmar[attempt[0].x][attempt[0].y].config(image = "", height = 1, width = 1)
                        sigmar[attempt[1].x][attempt[1].y].config(image = "", height = 1, width = 1)
                        attempt[0].copyTo(kingTarget)
                        attempt[1].copyTo(rookTarget)
                        attempt[0].type, attempt[0].color = 0, -1
                        attempt[1].type, attempt[1].color = 0, -1
                        sigmar[kingPos][attempt[0].y].config(image = imageCache[f"{king}"], height = 8, width = 8)
                        sigmar[rookPos][attempt[1].y].config(image = imageCache[f"{rook}"], height = 8, width = 8)
                        game.get(kingPos, attempt[0].y).moved = game.get(rookPos, attempt[1].y).moved = True
                    else:
                        kingPos = (attempt[0].y + attempt[1].y) // 2
                        rookPos = kingPos + 1
                        if attempt[0].y < attempt[1].y:
                            kingPos, rookPos = rookPos, kingPos
                        king = str(attempt[0])
                        rook = str(attempt[1])
                        # resetiraj prethodne pozicije
                        sigmar[attempt[0].x][attempt[0].y].config(image = "", height = 1, width = 1)
                        sigmar[attempt[1].x][attempt[1].y].config(image = "", height = 1, width = 1)
                        attempt[0].copyTo(game.get(attempt[0].x, kingPos))
                        attempt[1].copyTo(game.get(attempt[1].x, rookPos))
                        attempt[0].type, attempt[0].color = 0, -1
                        attempt[1].type, attempt[1].color = 0, -1
                        sigmar[attempt[0].x][kingPos].config(image = imageCache[f"{king}"], height = 8, width = 8)
                        sigmar[attempt[0].x][rookPos].config(image = imageCache[f"{rook}"], height = 8, width = 8)
                        game.get(attempt[0].x, kingPos).moved = game.get(attempt[1].x, kingPos).moved = True
                    changeTurn()
                # game.debug()
            # print("prešao")
        # print(attempt[0], attempt[1], attempt[0].first, attempt[1].first)
        # print(attempt[0], attempt[1])
        # print(attempt[0].color, attempt[1].color)

        if not game.authorizeMove(attempt[0], attempt[1]): return
        # provjeri za promocije
        if attempt[0].type == 1:
            if (attempt[0].color == 0 and attempt[0].y == 7) or (attempt[0].color == 1 and attempt[0].x == 6) or (attempt[0].color == 2 and attempt[0].y == 6) or (attempt[0].color == 3 and attempt[0].x == 7): 
               attempt[0].type = 5
               if actionType is None:
                   actionType = "promo"

        sigmar[attempt[1].x][attempt[1].y].config(image = imageCache[attempt[0].stringify()], height = 8, width = 8) # krađa identiteta
        attempt[0].copyTo(attempt[1]) # pretvori prvi u drugi
        # sad ubi originalnog
        destroyPiece(attempt[0])
        changeTurn()
        # provjeri jel šahmatiran igrač na potezu. Ako je, ubi sve kaj ima i voli
        while game.checkMate():
            eX, eY = None, None
            for i in range(14):
                for j in range(14):
                    if game.get(i,j).type == 6 and game.get(i,j).color == game.turn:
                        widget = sigmar[i][j]
                        eX = widget.winfo_x()
                        eY = widget.winfo_y()
            eX += (DISPLAY_WIDTH-850)//2 - 100
            eY += (DISPLAY_HEIGHT-800)//2 - 100
            actionType = "checkmate" # najnajveci prioritet lol
            SoundHandler.onCheckmate()
            explosion.explode(eX, eY)
            game.alive.remove(game.turn)
            # dodaj neki indikator lol
            print("Rikno", game.turn)
            for i in range(14):
                for j in range(14):
                    piece = game.get(j, i)
                    if piece.color == game.turn:
                        piece.color, piece.type = -1, 0
                        sigmar[piece.x][piece.y].config(image = "", height = 1, width = 1)
            changeTurn()
            if len(game.alive) == 1:
                SoundHandler.win()
                win.win(game.turn)
                prozor.quit()
            

        # updateaj stanja svih kraljeva (molicu ignorirati kako)
        for i in range(len(game.board)):
            for j in range(len(game.board[i])):
                for boja in game.alive:
                    if str(game.board[i][j]) == f"K{'RGYB'[boja]}":
                        # print(sigmar[j][i].cget("image"), imageCache[f"K{'RGYB'[boja]}+"])
                        if game.inDanger(boja) and not game.menga[boja]: 
                            print("mijenjam za", boja)
                            game.menga[boja] = True
                            if actionType != "checkmate": 
                                actionType = "check" # jači prioritet od svega koliko sam skuzio
                            sigmar[j][i].config(image = imageCache[f"K{'RGYB'[boja]}+"], height = 8, width = 8)
                            prozor.update()
                        elif not game.inDanger(boja):
                            print(boja, "siguran")
                            game.menga[boja] = False
                            sigmar[j][i].config(image = imageCache[f"K{'RGYB'[boja]}"], height = 8, width = 8)
                            prozor.update()
        attempt[1].moved = True
        prozor.update()
        if actionType is None:
            if raceGuesser == 0:
                actionType = "move"
            else:
                actionType = "take"
        
        # zvuk (castle + checkmate handlano odvojeno zbog strukture koda)
        # print(actionType)
        if actionType == "check": SoundHandler.onCheck()
        elif actionType == "promo": SoundHandler.onPromo()
        elif actionType == "take": SoundHandler.onTake()
        elif actionType == "move": SoundHandler.onMove()

selected = None # drzi "selektirani" objekt - move command zahtjeva dva klika, prvi selektira objekt, drugi izvrši move command

def tkMove(piece):
    
    global selected, game, sigmar
    # game.debug()
    # print(f"DANGER {game.turn}", game.inDanger())
    # print(selected, piece)
    if not selected:
        if piece.color != game.turn: # turn guard
            print("turn guard")
            return False
        if not piece.type: # blank guard
            print("blank guard")
            return False
        selected = piece
        button = sigmar[piece.x][piece.y]
        bgc = button.cget("bg")
        button.config(bg = colorSwitch(WHITE, BLACK, WHITESELECT, BLACKSELECT, bgc))
        # TODO: pokazi preview mogucih poteza
        # rough algoritam: dsl runnaj selected.checkMove za svako polje na mapi + check check
        # retractaj u else-u tako da storeas sve gumbove te samo reversas efekat
    else:
        # movecommand je issuan od selecteda do widgeta
        if selected.type == 6 and piece.type == 2 and selected.color == piece.color:
            stima = True # treba proci gore
        else: stima = selected.checkMove(piece)
        button = sigmar[selected.x][selected.y]
        bgc = button.cget("bg")
        button.config(bg = colorSwitch(WHITESELECT, BLACKSELECT, WHITE, BLACK, bgc))
        # game.debug()
        if not stima:
            selected = None
            return False
        else:
            cpy = selected
            selected = None
            
            return (cpy, piece)

    

prozor.grid()
for i in range (14):
    for j in range (14):
        if not (2<i<11 or 2<j<11):
            slika = Label(prozor, height = 4, width = 4, image = PhotoImage(file = r'.\Widgets\belo.png'))
            slika.grid(row = i, column = j)
            sigmar[j][i] = 'x'
            #veličina slike nije važna dok su dimenzije manje od gumba
        else:
            if ((i+j)%2==0):
                gumb = Button(prozor, bg=BLACK, height = 1, width = 1)
                boardButtonNames.append(str(gumb))
                sigmar[j][i] = gumb
                gumb.grid(row = i, column = j, ipadx=20, ipady=20)
                prozor.update()
                #print(gumb.winfo_width(), gumb.winfo_height()) #za pixel size gumba
            else:
                gumb = Button(prozor, bg=WHITE, height = 1, width = 1)
                sigmar[j][i] = gumb
                boardButtonNames.append(str(gumb))
                gumb.grid(row = i, column = j,  ipadx=20, ipady=20)
                prozor.update()
                #print(gumb.winfo_width(), gumb.winfo_height()) #za pixel size gumba

print("Smrt fašizmu!")






imageCache = dict() # jer je tkinter retardiran

for i in "PRBKNQ":
    for j in "RGBY":
        imageCache.update({(i + j) : PhotoImage(file = f".\\Widgets\\{i + j}.png")})
        if (i == 'K'): imageCache.update({(i + j + "+") : PhotoImage(file = f".\\Widgets\\{i + j}+.png")})

# nacrtaj početnu ploču
# NOTE: daljni updating će se odvijati tako da se samo updateaju stanja polja koja se u koraku promijene
board = game.board
for i in range(14):
    for j in range(14):
        # x = j, y = i
        pc = game.get(i, j).stringify()
        # print(pc)
        if (pc[0] in ['.', 'x']): continue # nije potrebno ništa
        sigmar[i][j].config(image = imageCache[pc], height = 8, width = 8)
        prozor.update()



def changeTurn():
    global turnLabel, prozor, game
    # goofy aah do while
    while True: 
        game.turn += 1
        game.turn %= 4
        if game.turn in game.alive:
            break
    turnLabel["text"] = (f"TURN {'RGYB'[game.turn]}")
    prozor.update()


# tButton = Button(prozor, bg="#322d57", height = 5, width = 15, text = "Promijeni turn", fg="white", font=("Courier New", 10), command=changeTurn)
# tButton.grid(row=20, column=20)

# def ballz():
#     global imageCache
#     imageCache.pop()


#     # test = Button(prozor, text="Public execution", height = 5, width = 5, command=ballz)
#     # test.grid(row = 3, column=15)
#     # prozor.update()

"""
foto=PhotoImage(file="Kg.png")
#label = Label(image = foto)
#label.image = foto
sigmar[0][4].config(image = foto, height=8, width=8)
                
prozor.update()
print(sigmar[0][4].winfo_width(), sigmar[0][4].winfo_height())

foto2=PhotoImage(file="Hg.png")
#label2 = Label(image = foto2)
#label2.image = foto2
sigmar[0][5].config(image = foto2, height=8, width=8)
                
prozor.update()
print(sigmar[0][5].winfo_width(), sigmar[0][5].winfo_height())
"""


prozor.bind('<ButtonPress-1>', goyim)
if GLOBAL_DEBUG: 
    prozor.bind('<Button-3>', genocid)
    prozor.bind('<Shift-Button-3>', genesis)
    prozor.bind('<a>', geneza)
    prozor.bind('')
    # prozor.bind('<b>', deebug)
prozor.mainloop()
