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
        if color == "white":
            return abs(end[0] - start[0]) <= 1 and end[1]-start[1] == 1
           
        if color == "black":
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
            



