class Piece:
       
    def __init__(self,side, label=""):
        self.position = None
        self.label = label
        self.color = side
        self.score = 0;
    def notConflict(self, board, color, start, end):
        pass
    def isInBound(self,end ):
        "checks if a position is on the board"
        return end[0] >= 0 and end[0] < 8 and end[1] >= 0 and end[1] < 8      
    def isValid(self, start, end, board,color):
        pass      
    def numberOfMoves(self,board, color, start):
        pass  
    def __repr__(self):
        return self.label

class Pawn (Piece):
    Y=[1,1,1]
    X=[0,-1,1]
    def __init__(self,side,label):
       
        Piece.__init__(self,side, label)
        self.score = 10

    def numberOfMoves(self,board, color, start):
        listOfMoves = []
        for i in range(len(self.X)):
            if color == "white":
                new_move = (start[0]+self.X[i], start[1]+self.Y[i])
            elif color == "black":
                new_move = (start[0]+self.X[i], start[1]-self.Y[i])
                
            if self.notConflict(board,color,start, new_move):
                listOfMoves.append(new_move)
        return listOfMoves

    def notConflict(self, board, color, start, end):
        if self.isInBound(end):
            if abs(end[0]-start[0]) == abs(end[1]-start[1]) :
                # if the pawn wants to move diagonally, then there must be an oponent occupies that location 
                if end in board and board[end].color != color:
                    return True
            else:
                # Check if there is any piece in front of it.
                return end not in board

        else:
            return False
            
    def isValid(self,start, end,board,color):
        initLocWhite = [(i,1) for i in range (8)]
        initLocBlack = [(i,6) for i in range (8)]
       
        if color == "white":
            if start in initLocWhite:
                return  abs(end[0] - start[0]) <= 1 and abs(end[1]-start[1]) <= 2  
            return abs(end[0] - start[0]) <= 1 and end[1]-start[1] == 1
           
        if color == "black":
            if start in initLocBlack:
                return  abs(end[0] - start[0]) <= 1 and abs(end[1]-start[1]) <= 2  
            return abs(end[0]-start[0]) <= 1  and start[1]-end[1] ==1
                

class Knight(Piece):
    X = [1, 1, -1, -1, 2, 2, -2, -2]
    Y = [2, -2, 2, -2, 1, -1, 1, -1]
    def __init__(self,side,label=""):
        Piece.__init__(self,side, label)
        self.score = 30

    def numberOfMoves(self,board, color, start):
        listOfMoves = []
        for i in range(len(self.X)):
            new_move = (start[0]+self.X[i], start[1]+self.Y[i])
            if self.notConflict(board,color,start, new_move):
                listOfMoves.append(new_move)
        return listOfMoves

    def notConflict(self, board, color, start, end):
        return  (self.isInBound(end) and  end not in board) or (end in board and board[end].color != self.color) 

    def isValid(self, start, end,board,color):
        deltaX = start[0] - end[0]
        deltaY = start[1] - end[1]
        for i in range(8):
            if deltaX == self.X[i] and deltaY == self.Y[i]:
                return True
        return False


class Rook(Piece): 
    def __init__(self,side,label=""):
        Piece.__init__(self,side, label)
        self.score = 50

    def numberOfMoves(self,board, color, start):
        listOfMoves = []
        for i in range(1,8):
            new_moves = [(start[0]+i,start[1]), (start[0]-i, start[1]), (start[0], start[1]+i), (start[0], start[1]-i)]
            for move in new_moves:
                if self.notConflict(board,color,start,move):
                    listOfMoves.append(move)
        return listOfMoves

    def notConflict(self, board, color, start, end):
        if self.isInBound(end):
            x = start[0]
            y = start[1]
            # print("Before",x,y)
            while (x,y) != end:
                if x != end[0]:
                    x= x-1 if x > end[0] else x+1
                elif y != end[1]:
                    y= y-1 if y > end[1] else y+1
                # print("After",x,y)
                if (x,y) in board:
                    if (x,y) == end:
                        return board[end].color != color
                    return False            
            return True 
        else: 
            return False
            
    def isValid(self,start, end,board,color):
        return  start[0] == end[0] or start[1] == end[1]

class Bishop(Piece):
    def __init__(self,side,label=""):
        Piece.__init__(self,side, label)
        self.score = 30

    def numberOfMoves(self,board, color, start):
        listOfMoves = []
        for i in range(1,8):
            new_moves = [(start[0]+i,start[1]+i), (start[0]-i,start[1]+i), (start[0]-i,start[1]-i), (start[0]+i, start[1]-i)]
            for move in new_moves:
                if self.notConflict(board,color,start,move):
                    listOfMoves.append(move)
        return listOfMoves
                
    def notConflict(self, board, color, start, end):
        if self.isInBound(end):
            x = start[0]
            y = start[1]

            while (x,y) != end:
                x= x+1 if x < end[0] else x-1
                y= y+1 if y < end[1] else y-1

                if (x,y) in board:
                    if (x,y) == end:
                        return board[end].color != color
                    return False            
            return True 
        else: 
            return False

     
    def isValid(self, start, end,board,color):
        return  abs(start[0] - end[0]) == abs(end[1] - start[1])
            
class Queen(Piece): 
    def __init__(self,side,label):
        Piece.__init__(self,side, label)
        self.score = 90

    def numberOfMoves(self, board, color,start):
        r = Rook(color)
        b = Bishop(color)
        return r.numberOfMoves(board,color,start)+ b.numberOfMoves(board,color,start)


    def notConflict(self, board, color, start, end):
        if (abs(start[0]-end[0]) == abs(start[1] - end[1])):
            # Queen will move diagonally apply Bishop logic
            b = Bishop(color)
            if  not b.notConflict(board,color,start,end):
                return False
        else:
            # Will move like a rook
            r = Rook(color)
            if not r.notConflict(board,color,start,end):
                return False
        return True

    def isValid(self, start, end,board, color):
        return start[0] == end[0] or start[1] == end[1] or abs(start[0]- end[0]) == abs(start[1]-end[1])
        
class King(Piece):
    X= [1,-1,-1,+1,0,1]
    Y= [1,1,-1,-1,1,0]
    def __init__(self,side,label):
        Piece.__init__(self,side, label)
        self.score = 900
    
    def numberOfMoves(self, board, color,start):
        listOfMoves = []
        for i in range(len(self.X)):
            new_move = (start[0]+self.X[i], start[1]+self.Y[i])
            if self.notConflict(board,color,start, new_move):
                listOfMoves.append(new_move)
        return listOfMoves
        
    def notConflict(self, board, color, start, end):
        if self.isInBound(end):
            if end in board:
                return board[end].color != self.color
            return True
        return False

    def isValid(self, start, end,board,color):
        return  abs(start[0]-end[0]) <= 1 and abs(start[1]-end[1]) <= 1
            





WHITE = "white"
BLACK = "black"
TERMINATE = (-1,-1),(-1,-1)
DEPTH = 2 # Lower depth means AI will play better

class Controller:
    
    uniDict = {
    WHITE : {Pawn : "♙", Rook : "♖", Knight : "♘", Bishop : "♗", King : "♔", Queen : "♕" }, 
    BLACK : {Pawn : "♟", Rook : "♜", Knight : "♞", Bishop : "♝", King : "♚", Queen : "♛" }
    
    }

    def __init__(self):
        self.board = {}
        self.initPieces()
        self.playersTurn = BLACK
        #self.printBoard()
        self.prompt = "Pick the move"
        self.gameRun()


    def initPieces(self):
        for i in range (0,8):
            self.board[(i,1)] = Pawn(WHITE, self.uniDict[WHITE][Pawn])
            self.board[(i,6)] = Pawn(BLACK, self.uniDict[BLACK][Pawn])
        placers = [Rook,Knight,Bishop,Queen,King,Bishop,Knight,Rook]   
        for i in range(0,8):
            self.board[(i,0)] = placers[i](WHITE,self.uniDict[WHITE][placers[i]])
            self.board[((7-i),7)] = placers[i](BLACK,self.uniDict[BLACK][placers[i]])
        placers.reverse()

    def gameRun(self):
        while (True):
            self.printBoard1()
            if self.playersTurn == BLACK:
                print(self.prompt)
                s, e = self.parseInput()
            elif self.playersTurn == WHITE:
                print("CPU is thinking . . . . . . ")
                move = self.AI_pickTheMove(self.board,3)
                s= move[0]
                e= move[1]

            try:
                target = self.board[s]
            except:
                print("Can't find that piece")
                continue
                
            if target.isValid(s,e,self.board, target.color) and target.notConflict(self.board,target.color,s,e):
                self.board[e] = self.board[s] # Assign a position with new piece
                del self.board[s] # Remove the picked piece

                self.isCheck()
                if self.playersTurn == WHITE:
                    self.playersTurn = BLACK
                else:
                    self.playersTurn = WHITE

            else:
                print("Invalid move")
           

  
    def isCheck(self):
        #check where the kings are, check all opposing color against those kings, then if either get hit.
        king = King
        kingDict = {}
        pieceDict = {BLACK : [], WHITE : []}
        for position,piece in self.board.items():
            if type(piece) == King:
                kingDict[piece.color] = position
            pieceDict[piece.color].append((piece,position))
        #white
        if self.checkKing(kingDict[WHITE],pieceDict[BLACK]):
            self.message = "White player is in check"
        if self.checkKing(kingDict[BLACK],pieceDict[WHITE]):
            self.message = "Black player is in check"
        
        
    def checkKing(self,kingpos,piecelist):
        #checks if any pieces in piece list can see the king in kingpos
        for piece,position in piecelist:
            if piece.isValid(position,kingpos,self.board,piece.color):
                return True

    # AI PART
    
    def AI_pickTheMove(self,board,depth):
        next_move = self.mini_maxRoot(board,DEPTH)
        print ("AI next move:", next_move)
        return next_move

    def heuristic(self,board):
        heuristic = 0
        # geting heuristic value
        # f(P) = 9(Q-Q') + 5(R-R') + 3(B-B'+N-N') + (P-P') - 0.5(D-D'+S-S'+I-I') + 0.1(M-M') 
        """
            TODO: heuristic function needs some more works to become a Grand Master ^^
        """
        for position, piece in board.items():
            if piece.color == BLACK:
                heuristic += piece.score
                heuristic += len(piece.numberOfMoves(board, piece.color, position))
            elif piece.color == WHITE:
                heuristic -= piece.score
                heuristic -= len(piece.numberOfMoves(board, piece.color, position))
        return heuristic

 
    def moveable(self, board,color):
        possibleMoves = []
        for location, piece in board.items():
            if piece.color == color and len(piece.numberOfMoves(board,piece.color,location)) >0:
                possibleMoves.append(location)
        return possibleMoves

    def mini_maxRoot(self,board,depth):
        legalMoves = self.moveable(board,WHITE)
        bestMove = 9999
        finalMove = 0
        bestMoveFinal = 0
        for pieceLoc in legalMoves:
            # Evaluate each piece in the board
            clone = board.copy()
            # make a move
            piece = clone[pieceLoc]
            possibleMoves = piece.numberOfMoves(clone,piece.color,pieceLoc)
            for move in possibleMoves:
                clone[move] = piece
                del clone[pieceLoc]
                value = min(bestMove, self.mini_max(clone,True,-99999,99999,depth))
                # print(value)
                if (value < bestMove):
                    bestMove = value
                    bestMoveFinal = value
                    finalMove = pieceLoc, move
                clone = board.copy()
                # pieceLoc = move
        return finalMove
   
    def mini_max(self,board,maxTurn,alpha, beta,currDepth):
        if currDepth == 0:
            # self.printBoard_debug(board)
            return self.heuristic(board)
        
        if maxTurn:
            # print("black: ",currDepth)
            posibleMoves = self.moveable(board,BLACK)
            value = -9999
            for pieceLoc in posibleMoves: 
                piece = board[pieceLoc]
                moves = piece.numberOfMoves(board,piece.color,pieceLoc)
                for move in moves:
                    clone = board.copy()
                    clone[move] = piece
                    del clone[pieceLoc]
                    value = max(value,self.mini_max(clone, False, alpha,beta, currDepth-1))
                    alpha = max(alpha,value)
                    if alpha >= beta:
                        break
            return value
        else:
            value = 9999
            posibleMoves = self.moveable(board,WHITE)
            for pieceLoc in posibleMoves:
                piece = board[pieceLoc]
                moves = piece.numberOfMoves(board,piece.color,pieceLoc)
                for move in moves:
                    clone = board.copy()                        
                    clone[move] = piece
                    del clone[pieceLoc]
                    value = min(value,self.mini_max(clone, True, alpha,beta, currDepth-1))
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
            return value

            

    def parseInput(self):
        try:
            a,b = input().split()
            a = (int(a[0]), int(a[1]))
            b = (int(b[0]), int(b[1]))
        
            print(a,b)
            return (a,b)
        except:
            print("error decoding input. please try again")
            return((-1,-1),(-1,-1))

    def printBoard1(self):
        for i in range(0,8):
            print("\n ","-"*40)
            print(i,end=" | ")
            for j in range(0,8):
                item = self.board.get((j,i)," ")
                print(str(item)+' | ', end = " ")
        print("\n ","-"*40)
        print("  ", end="| ")
        for i in range(0,8):
            print(str(i)+' | ', end = " ")
        print("\n ","-"*40)

   
    
    """
        TODO: fix bugs function double_prawns
    
    # def double_pawns(self,board):
    #     # return number of white and black double pawns positions
    #     doublePawns_black,foundBlack = 0,0
    #     doublePawns_white,foundWhite = 0,0
    #     for file in range(0,8):
    #         temp_black = -1
    #         temp_white = -1
    #         for y in range(0,8):
    #             if (file,y) in board:
    #                 if board[(file,y)].label == self.uniDict[WHITE][Pawn]:
    #                     temp_white+=1
    #                     foundWhite = 1
    #                 elif board[(file,y)].label == self.uniDict[BLACK][Pawn]:
    #                     temp_black+=1
    #                     foundBlack = 1
                    

    #         doublePawns_black+=temp_black
    #         doublePawns_white+=temp_white
        
    #     print("DB_Black: ",doublePawns_black)
    #     print("DB_White: ",doublePawns_white)
                
    #     if (not foundBlack):
    #         return doublePawns_white
    #     elif (not foundWhite):
    #         return doublePawns_black
        
    #     return doublePawns_black-doublePawns_white 
    modifying comments in modifying comments branch

    """




Controller()
