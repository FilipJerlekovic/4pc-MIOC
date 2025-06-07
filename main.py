from tkinter import *
from tkinter import font

from simulator import Chess, Piece


game = Chess()
game.setupBoard()

prozor = Tk()
global_font=("Courier New", 5)
prozor.option_add("*Font", global_font)

WHITE = "#cbd6ce"
BLACK = "#7d7d7d"
WHITESELECT = "#a6a283"
BLACKSELECT = "#595741"

GLOBAL_DEBUG = True



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


def colorSwitch(primary1, primary2, secondary1, secondary2, check):
    if check == primary1: return secondary1
    elif check == primary2: return secondary2
    else: return check # nista
    
    
def genocid(event):
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
        # castling check
        if attempt[0].color == attempt[1].color and attempt[0].type == 6 and attempt[1].type == 2: # castle check
            print("bombardiro corooridlo")
            if not (attempt[0].moved or attempt[1].moved): # move check
                print("tralalellotllarlarlalral")
                # TODO: dodaj check check
                # blank check
                flag = True
                if attempt[0].color in [0, 2]:
                    for i in range(min(attempt[0].x, attempt[1].x) + 1, max(attempt[0].x, attempt[1].x) - 1):
                        if game.get(i, attempt[0].y).type != 0:
                            flag = False
                            break
                else:
                    for i in range(min(attempt[0].y, attempt[1].y) + 1, max(attempt[0].y, attempt[1].y) - 1):
                        if game.get(i, attempt[0].y).type != 0:
                            flag = False
                            break
                
                if flag: 
                    # switchaj 
                    kingPos, rookPos = None, None
                    if attempt[0].color in [0,2]:
                        kingPos = (attempt[0].x + attempt[1].x) // 2
                        rookPos = kingPos
                        if attempt[0].x < attempt[1].x: kingPos += 1
                        else: rookPos += 1
                        king = str(attempt[0])
                        rook = str(attempt[1])
                        # resetiraj prethodne pozicije
                        sigmar[attempt[0].x][attempt[0].y].config(image = "", height = 1, width = 1)
                        sigmar[attempt[1].x][attempt[1].y].config(image = "", height = 1, width = 1)
                        attempt[0].copyTo(attempt[0].chessObj.get(kingPos, attempt[0].y))
                        attempt[0].type, attempt[0].color = 0, -1
                        sigmar[kingPos][attempt[0].y].config(image = imageCache[f"{king}"], height = 8, width = 8)
                        sigmar[rookPos][attempt[1].y].config(image = imageCache[f"{rook}"], height = 8, width = 8)
                        game.get(kingPos, attempt[0].y).moved = game.get(rookPos, attempt[1].y).moved = True
                    else:
                        kingPos = (attempt[0].y + attempt[1].y) // 2
                        rookPos = kingPos + 1
                        king = str(attempt[0])
                        rook = str(attempt[1])
                        # resetiraj prethodne pozicije
                        sigmar[attempt[0].x][attempt[0].y].config(image = "", height = 1, width = 1)
                        sigmar[attempt[1].x][attempt[1].y].config(image = "", height = 1, width = 1)
                        attempt[0].copyTo(attempt[0].chessObj.get(attempt[0].x, kingPos))
                        attempt[0].type, attempt[0].color = 0, -1
                        sigmar[attempt[0].x][kingPos].config(image = imageCache[f"{king}"], height = 8, width = 8)
                        sigmar[attempt[0].x][rookPos].config(image = imageCache[f"{rook}"], height = 8, width = 8)
                        game.get(attempt[0].x, kingPos).moved = game.get(attempt[1].x, kingPos).moved = True
                # changeTurn()
                return
        print(attempt[0], attempt[1])
        
        if attempt[1].type == 6: return # regicid je kriminal
        if game.checkPin(attempt[0], attempt[1]): return # pokušaj regicida
        if attempt[0].canEat(attempt[1]): return # kanibalizam
        if (game.inDanger() and game.checkPin(attempt[0], attempt[1])): 
            return False # i sacrifice my life for pakistan aaah linija
        # TODO: nemoj kompletno ignorirati castleanje i en passant

        # provjeri za promocije
        if attempt[0].type == 1:
            if (attempt[0].color == 0 and attempt[0].y == 7): attempt[0].type = 5
            if (attempt[0].color == 1 and attempt[0].x == 6): attempt[0].type = 5
            if (attempt[0].color == 2 and attempt[0].y == 6): attempt[0].type = 5
            if (attempt[0].color == 3 and attempt[0].x == 7): attempt[0].type = 5
        sigmar[attempt[1].x][attempt[1].y].config(image = imageCache[attempt[0].stringify()], height = 8, width = 8) # krađa identiteta
        attempt[0].copyTo(attempt[1]) # pretvori prvi u drugi
        # sad ubi originalnog
        attempt[0].type = 0
        attempt[0].color = -1
        sigmar[attempt[0].x][attempt[0].y].config(image = "", height = 1, width = 1)
        changeTurn()

        # updateaj stanja svih kraljeva (molicu ignorirati kako)
        for i in range(len(game.board)):
            for j in range(len(game.board[i])):
                for boja in game.alive:
                    if str(game.board[i][j]) == f"K{'RGYB'[boja]}":
                        if game.inDanger(boja): 
                            print("mijenjam za", boja)
                            sigmar[j][i].config(image = imageCache[f"K{'RGYB'[boja]}+"], height = 8, width = 8)
                            prozor.update()
                        else:
                            sigmar[j][i].config(image = imageCache[f"K{'RGYB'[boja]}"], height = 8, width = 8)
                            prozor.update()
        attempt[1].moved = True
        prozor.update()

selected = None # drzi "selektirani" objekt - move command zahtjeva dva klika, prvi selektira objekt, drugi izvrši move command

def tkMove(piece):
    
    global selected, game, sigmar
    game.debug()
    print(f"DANGER {game.turn}", game.inDanger())
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






imageCache = {} # jer je tkinter retardiran

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
    global turnLabel, prozor
    game.turn += 1
    game.turn %= 4
    turnLabel["text"] = ("TURN " + "RGYB"[game.turn])
    prozor.update()


# tButton = Button(prozor, bg="#322d57", height = 5, width = 15, text = "Promijeni turn", fg="white", font=("Courier New", 10), command=changeTurn)
# tButton.grid(row=20, column=20)

def ballz():
    global imageCache
    imageCache.pop()


    # test = Button(prozor, text="Public execution", height = 5, width = 5, command=ballz)
    # test.grid(row = 3, column=15)
    # prozor.update()

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
if GLOBAL_DEBUG: prozor.bind('<ButtonPress-3>', genocid)
prozor.mainloop()
