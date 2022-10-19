import heapq
import numpy as np
import random
from Bot import Bot
from GameAction import GameAction
from GameState import GameState
from Nodes import Nodes
from timeout_decorator import exit_after

class MinimaxBot(Bot):

    #### GET ACTION
    # Metode yang digunakan untuk mencari tahu aksi yang akan dilakukan oleh bot
    # Return:
    #   GameAction
    def get_action(self, state: GameState) -> GameAction:
        self.player1_turn = state.player1_turn
        count = 0
        for i in range (3):
            for j in range (4) :
                if state.row_status[j,i] == 1:
                    count += 1
        for i in range (4):
            for j in range (3):
                if state.col_status[j,i] == 1:
                    count += 1
        count = 24-count

        Node = Nodes(state.board_status, state.row_status, state.col_status, state.player1_turn)

        try:
            action = self.get_minimax_action(Node, count, 1)
        except KeyboardInterrupt:
            print("timed out")
            return self.get_random_action(state)
        return action 
    
    #### DYNAMIC DEPTH LIMIT
    # Metode yang digunakan untuk menentukan batas kedalaman pencarian
    # Return:
    #   int
    def dynamic_depth_limit(self, depth) -> int:
        if depth < 8:
          return 4
        elif depth < 12:
          return 5
        elif depth < 15:
          return 6
        elif depth < 16:
          return 7
        else:
          return 8

    #### GET MINIMAX ACTION
    # Metode yang digunakan untuk mencari tahu aksi yang akan diambil
    # dengan mengimplementasikan algoritma minimax dan alpha beta pruning
    # Return:
    #   GameAction
    @exit_after(5)
    def get_minimax_action(self, Node, Height, Depth):
        for i in range (3):
            for j in range (4):
                if Node.Current.row_status[j,i] == 0 and (i,j,"row") not in Node.Positions:
                    Node.Make(i, j, "row", self.player1_turn)
                    if Height < 2 :
                        return GameAction("row", (i,j))

        for i in range (4):
            for j in range (3):
                if Node.Current.col_status[j,i] == 0 and (i,j,"col") not in Node.Positions:
                    Node.Make(i, j, "col", self.player1_turn)
                    if Height < 2 :
                        return GameAction("col", (i,j))

        MaxScore = -1000
        i = 0
        j = 0
        rowcol = ""
        initialDepthLimit = self.dynamic_depth_limit(24-Height)
        for _ in range(len(Node.Children)):
            data = heapq.heappop(Node.Children)
            k = data.Position
            z = data
            Result = self.Minimum(z, Height - 1, MaxScore, Depth+1, initialDepthLimit)
            if MaxScore < Result:
                MaxScore = Result
                i = k[0]
                j = k[1]
                rowcol = k[2]
        return GameAction(rowcol, (i,j))

    #### MAXIMUM
    # Metode yang digunakan untuk mencari nilai maksimum dari suatu node
    # Return:
    #   int
    def Maximum(self, Node, Height, Alpha, Depth, DepthLimit):
        if Height == 0 or Depth == DepthLimit:
            return Node.CurrentScore
        
        for i in range (3):
            for j in range (4):
                if Node.Current.row_status[j,i] == 0 and (i,j,"row") not in Node.Positions:
                    Node.Make(i, j, "row", self.player1_turn)

        for i in range (4):
            for j in range (3):
                if Node.Current.col_status[j,i] == 0 and (i,j,"col") not in Node.Positions:
                    Node.Make(i, j, "col", self.player1_turn)

        Minimum_Score = 1000
        Maximum_Score = -1000
        for _ in range(len(Node.Children)):
            z = heapq.heappop(Node.Children)    
            if Node.Current.player1_turn == z.Current.player1_turn:
                Result = self.Maximum(z, Height - 1, Minimum_Score, Depth+1, DepthLimit)
                if Minimum_Score > Result:
                    Minimum_Score = Result
            else:
                Result = self.Minimum(z, Height - 1, Maximum_Score, Depth + 1, DepthLimit)
            
            if Maximum_Score < Result:
                Maximum_Score = Result
            if Result > Alpha:
                return Result

        return Maximum_Score

    #### MINIMUM
    # Metode yang digunakan untuk mencari nilai minimum dari suatu node
    # Return:
    #   int
    def Minimum(self, Node, Height, Beta, Depth, DepthLimit):
        if Height == 0 or Depth == DepthLimit:
            return Node.CurrentScore
        
        for i in range (3):
            for j in range (4):
                if Node.Current.row_status[j,i] == 0 and (i,j,"row") not in Node.Positions:
                    Node.Make(i, j, "row", self.player1_turn)

        for i in range (4):
            for j in range (3):
                if Node.Current.col_status[j,i] == 0 and (i,j,"col") not in Node.Positions:
                    Node.Make(i, j, "col", self.player1_turn)
                    
        Maximum_Score = -1000
        Minimum_Score = 1000
        for _ in range(len(Node.Children)):
            z = heapq.heappop(Node.Children)
            if Node.Current.player1_turn == z.Current.player1_turn:
                Result = self.Minimum(z, Height - 1, Maximum_Score, Depth + 1, DepthLimit)
                if Maximum_Score < Result:
                    Maximum_Score = Result
            else:
                Result = self.Maximum(z, Height - 1, Minimum_Score, Depth + 1, DepthLimit)
            
            if Minimum_Score > Result:
                Minimum_Score = Result
            if Result < Beta:
                return Result
                
        return Minimum_Score

    def get_random_action(self, state: GameState) -> GameAction:
        if random.random() < 0.5:
            return self.get_random_row_action(state)
        else:
            return self.get_random_col_action(state)

    def get_random_row_action(self, state: GameState) -> GameAction:
        position = self.get_random_position_with_zero_value(state.row_status)
        return GameAction("row", position)

    def get_random_position_with_zero_value(self, matrix: np.ndarray):
        [ny, nx] = matrix.shape

        x = -1
        y = -1
        valid = False
        
        while not valid:
            x = random.randrange(0, nx)
            y = random.randrange(0, ny)
            valid = matrix[y, x] == 0
        
        return (x, y)

    def get_random_col_action(self, state: GameState) -> GameAction:
        position = self.get_random_position_with_zero_value(state.col_status)
        return GameAction("col", position)
