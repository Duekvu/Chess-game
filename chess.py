from Pawn import Pawn
from Pawn import King
from Pawn import Knight
from Pawn import Queen
from Pawn import Bishop
from Pawn import Rook
import itertools
import random


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

    # enumurating numbers of move avaliable for the computer
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

    """




Controller()
