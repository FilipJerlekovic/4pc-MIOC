import copy

class Piece:
    def __init__(self, x, y, pc = 0, clr = -1, chessObj = None): # Piece: -1 = out, 0 blank, 1p, 2r, 3n, 4b, 5q, 6k, Color: 0r, 1g, 2y, 3b, -1 blank
        self.type = pc
        self.color = clr
        self.moved = 0 # king rook
        self.first = True # pawn
        self.x = x
        self.y = y
        self.chessObj = chessObj

    def copyTo(self, other): # osim x y jer ce to ubit sve
        other.type = self.type
        other.color = self.color
        other.moved = self.moved
        other.first = self.first
    
    def stringify(self):
        clr = ["R", "G", "Y", "B"]
        piece = [".","P", "R", "N", "B", "Q", "K", "x"]
        return f"{piece[self.type]}{clr[self.color] if self.color != -1 else '?'}"

    def __str__(self):
        return self.stringify()
    def canEat(self, other):
        if self.color == other.color: return False
        # TODO: add check check
        return True
        
    def _checkRQB(self, move, toX, toY): # updateaj mapu napadnutih figura na ploci
        gurt = ""
        if ( self.chessObj.get(toX, toY).type == -1 or ( self.chessObj.get(toX, toY).color == self.color)): 
            gurt = "yo" # nemore se ubit niti bit kanibalisticke naravi
            #print("gurt: yo")
        # print(f"Starting at: X={self.x}; Y={self.y} ({ self.chessObj.get(self.x, self.y)})")
        # print(f"Target at: X={toX}; Y={toY} ({self.chessObj.get(toX, toY)})")
        ret = False
        for i in move:
            dX = i[1]
            dY = i[0]
            while ((self.x + dX in range(0, 14)) and (self.y + dY in range(0, 14))):
                nX = self.x + dX
                nY = self.y + dY
                if (self.chessObj.get(nX, nY).type == -1): break
                # print(f"CHECKING COORDS: X={nX}; Y={nY} ({self.chessObj.get(nX, nY)})")
                if ((toX == self.x + dX) and (toY == self.y + dY)): ret = True
                if ( self.chessObj.get(nX, nY).type != 0): break # blokira
                
                dX += i[1]
                dY += i[0]
        return False if gurt else ret
    
    def _njort(self, toX, toY):
        flag = False
        move = [(-2, 1), (-2, -1), (1, -2), (1, 2), (-1, -2), (-1, 2), (2, -1), (2, 1)]
        for i in move:
            nX = self.x + i[0]
            nY = self.y + i[1]
            if ((nX not in range(0, 14)) or (nY not in range(0, 14)) or (self.chessObj.get(nX, nY).type == -1)): continue
            if (nX == toX) and (nY == toY): flag = True
        return flag

    def _feudalismAndItsConsequences(self, toX, toY):
        #print(self.first)
        move = [ [0, -1], [0, -2]]
        attack = [[1,-1], [-1, -1]]
        coeff = [[1,1], [1,-1], [1, -1], [-1, 1]]
        if self.color: # cba
            if self.color & 1: 
                for i in range(2):
                    move[i][0], move[i][1] = move[i][1], move[i][0]
                    attack[i][0], attack[i][1] = attack[i][1], attack[i][0]
            for i in range(2):
                move[i][0] *= coeff[self.color][0]
                move[i][1] *= coeff[self.color][1]
                attack[i][0] *= coeff[self.color][0]
                attack[i][1] *= coeff[self.color][1]
        for i in attack:
            nx = self.x + i[0]
            ny = self.y + i[1]
            if not (nx in range(14) and ny in range(14) or (self.chessObj.get(nx, ny).type == -1)): continue
        # double
        if self.first and self.x + move[1][0] == toX and self.y + move[1][1] == toY:
            # provjeri da je zapravo sve slobodno
            if self.chessObj.get(self.x + move[0][0], self.y + move[0][1]).type or self.chessObj.get(self.x + move[1][0], self.y + move[1][1]).type: # nesto blokira
                return False
            self.first = False
            return True
        #single
        if self.x + move[0][0] == toX and self.y + move[0][1] == toY: 
            if self.chessObj.get(self.x + move[0][0], self.y + move[0][1]).type: # nesto blokira
                return False
            self.first = False
            return True
        # attack je jedino bitan za slucajeve kada mozes jesti
        for i in attack:
            nx = self.x + i[0]
            ny = self.y + i[1]
            if not (nx in range(14) and ny in range(14)): continue
            if self.chessObj.get(nx, ny).type not in [-1, 0, 6] and self.chessObj.get(nx, ny).color != self.color:
                if nx == toX and ny == toY: 
                    self.first = False
                    return True
        return False
    
    def _kingTerryTheTerrible(self, toX, toY):
        # TODO: check check
        flag = False
        move = [ (0, 1), (0, -1), (1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1)]
        for i in move:
            nX = self.x + i[0]
            nY = self.y + i[1]
            if ((nX not in range(0, 14)) or (nY not in range(0, 14)) or (self.chessObj.get(nX, nY).type == -1)): continue
            if (nX == toX) and (nY == toY): flag = True
        return flag
    
    def checkMove(self, other):
        if not other: return False # uuuuuuuuuh
        toX, toY = other.x, other.y
        ml = [(1, 0), (-1, 0), (0, 1), (0, -1),   (1, 1), (1, -1), (-1, 1), (-1, -1)]
        if self.type == 3: return self._njort(toX, toY)
        if self.type == 2: return self._checkRQB(ml[:4], toX, toY) # r
        elif self.type == 4: return self._checkRQB(ml[4:], toX, toY) # b
        elif self.type == 5: return self._checkRQB(ml, toX, toY) # q
        elif self.type == 1: return self._feudalismAndItsConsequences(toX, toY)
        elif self.type == 6: return self._kingTerryTheTerrible(toX, toY)
        else: return False
            

class Chess:
    def __init__(self):
        self.board = []
        self.alive = [0, 1, 2, 3]
        self.castleable = [1,1,1,1]
        self.turn = 0
    
    def get(self, x, y):
        # print(x, y)
        return self.board[y][x]
    
    def set(self, x, y, type = -1, color = -1):
        self.get(x, y).type = type
        self.get(x, y).color = color
    
    def debug(self):
        for i in range(14):
            for j in range(14):
                print(self.get(j, i), end=" ")
            print()
    def setupBoard(self):
        board = []
        order = [2,3,4,6,5,4,3,2]
        for i in range(14):
            row = []
            for j in range(14):
                row.append(Piece(j, i, chessObj=self))
            board.append(row)
        
        for i in range(8): # top
            board[0][3 + i].type = order[i]
            board[1][3 + i].type = 1
            board[1][3 + i].color = 2
            board[0][3 + i].color = 2
        for i in range(8): # left
            board[i+3][0].type = order[i]
            board[i+3][1].type = 1
            board[i+3][1].color = 3
            board[i+3][0].color = 3
        order.reverse()
        for i in range(8): # bottom
            board[13][3 + i].type = order[i]
            board[12][3 + i].type = 1
            board[12][3 + i].color = 0
            board[13][3 + i].color = 0
        for i in range(8): # left
            board[i+3][13].type = order[i]
            board[i+3][12].type = 1
            board[i+3][13].color = 1
            board[i+3][12].color = 1
        for i in range(3):
            for j in range(3):
                board[i][j].type = board[i][13-j].type = -1
        for i in range(3):
            for j in range(3):
                board[13-i][j].type = board[13-i][13-j].type = -1
        self.board = board
        
    # def move(self, start, end, check = False):
    #     p1 = self.board[start[0]][start[1]]
    #     p2 = self.board[end[0]][end[1]]
        
    #     stype = p1.type
    #     scolor = p1.color
        
    #     etype = p2.type
    #     ecolor = p2.color
        
    #     if (stype == -1) or (stype == 0) or (etype == -1): return -1 # ????
    #     # special case: castling -> move unmoved king to own unmoved rook
    #     if (scolor == ecolor) and (stype == 6 and etype == 1):
    #         if p1.moved or p2.moved: return 0
    #         # check if empty
    #         if scolor in [0, 2]:
    #             for i in range(min(start[0], end[0])+1, max(start[0], end[0])-1):
    #                 if self.board[i][start[1]].type != 0: return 0
    #         if not check:
    #             med = (p1.x + p2.x) / 2
    #             p1.x = med
    #             p2.x = med - 1
    #         return 1
        
    def inDanger(self, who=None):
        if not who: who = self.turn
        # pronadi kralja onog na potezu
        monarh = None
        for i in range(14):
            for j in range(14):
                pc = self.get(j, i)
                if pc.type == 6 and pc.color == who:
                    monarh = pc
                    break
        print(monarh)
        # uuuuh
        for i in range(14):
            for j in range(14):
                if self.get(j, i).checkMove(monarh): return True
        return False
    
    def checkPin(self, start, end): # lord have mercy
        # NOTE: ova funkcija podrazumijeva to da nisi vec u sahu te da je potez start->beginning legalan po drugim kriterijima
        # pinnan je ako samom sebi zada sah ako se Piece start pomakne do Piecea beginning (ilegalno)
        
        # na koju sam ja foru bio prvi na drzavnom kodirajuci ovako genijalne algoritme jaoo

        # simuliraj pomak 
        sX, sY, eX, eY = start.x, start.y, end.x, end.y
        second = self.board[eY][eX]
        first = self.board[sY][sX]
        cpy = copy.copy(first)
        first.copyTo(second)
        first.type, first.color = 0, -1

        pin = self.inDanger() # provjera
        print(cpy, first)
        # retrack
        cpy.copyTo(first)
        second.type, second.color = 0, -1
        print(first, second)

        return pin
    

if __name__ == "__main__":
    game = Chess()
    game.setupBoard()
    
    #game.get(8, 8).type = 2
    # game.get(8, 8)._checkRQB( [(1, 0), (-1, 0), (0, 1), (0, -1),   (1, 1), (1, -1), (-1, 1), (-1, -1)], 5, 0, game)
    # game.get(8, 8)._njort(10, 10, game)
    # game.get(8,8).color = 3
    # game.get(8, 8)._feudalismAndItsConsequences(10, 10, game)
    #game.generateDangerBoard(0)
    #game.get(8,8)._kingTerryTheTerrible(10, 10, game)
    
    game.debug()    
