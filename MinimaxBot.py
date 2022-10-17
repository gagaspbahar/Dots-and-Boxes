import heapq
from operator import indexOf
from time import time
from Bot import Bot
from GameAction import GameAction
from GameState import GameState
from Nodes import Nodes

class MinimaxBot(Bot):
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

        # Node = Nodes(state.board_status, state.row_status, state.col_status, state.player1_turn, minimax, currentScore, position)
        Node = Nodes(state.board_status, state.row_status, state.col_status, state.player1_turn)
        return self.get_minimax_action(Node, count, 1)  
    
    def dynamic_depth_limit(self, depth) -> int:
        if depth < 8:
          return 4
        # if depth == 5:
        #   return 5
        elif depth < 12:
          return 5
        # elif depth == 11:
        #   return 7
        elif depth < 15:
          return 6
        elif depth < 16:
          return 7
        else:
          return 25 - depth


    def get_minimax_action(self, Node, Height, Depth):
        start = time()
        print('==================new action')
        for i in range (3):
            for j in range (4):
                if Node.Current.row_status[j,i] == 0 and (i,j,"row") not in Node.Positions:
                    Node.Make(i, j, "row", self.player1_turn)
                    # print("row", i, j)
                    # print(Node.Children[(i, j, "row")])
                    if Height < 2 :
                        return GameAction("row", (i,j))

        for i in range (4):
            for j in range (3):
                if Node.Current.col_status[j,i] == 0 and (i,j,"col") not in Node.Positions:
                    Node.Make(i, j, "col", self.player1_turn)
                    # print("col", i, j)
                    # print(Node.Children[(i, j, "col")])
                    if Height < 2 :
                        return GameAction("col", (i,j))

        MaxScore = -1000
        # MinScore = 1000
        i = 0
        j = 0
        rowcol = ""
        initialDepthLimit = self.dynamic_depth_limit(24-Height)
        print("depth: ", initialDepthLimit)
        print("turn: ", 24-Height)
        # for _, z in Node.Children.items():
        for _ in range(len(Node.Children)):
            # Result = self.Maximum(z, Height - 1, Minimum_Score, Depth+1)
            data = heapq.heappop(Node.Children)
            k = data.Position
            z = data
            Result = self.Minimum(z, Height - 1, MaxScore, Depth+1, initialDepthLimit)
            print(k, " ", Result)
            # if Minimum_Score > Result:
            #     Minimum_Score = Result
            #     i = k[0]
            #     j = k[1]
            #     rowcol = k[2]
            if MaxScore < Result:
                MaxScore = Result
                i = k[0]
                j = k[1]
                rowcol = k[2]
            # print("min: ", Minimum_Score)
            print("max: ", MaxScore)
            print("treeline", data.ScoreWithThreeline)

        # print(rowcol, (i,j))
        print("timetaken:", time() - start)
        print("taken: ", rowcol, (i,j))
        return GameAction(rowcol, (i,j))

    def Maximum(self, Node, Height, Alpha, Depth, DepthLimit):
        # print(Height)
        if Height == 0 or Depth == DepthLimit:
            # print(Node.CurrentScore)
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

    def Minimum(self, Node, Height, Beta, Depth, DepthLimit):
        # print(Height)
        if Height == 0 or Depth == DepthLimit:
            # print(Node.CurrentScore)
            return Node.CurrentScore

        # if Depth == 5:
        #     player1_score = len(np.argwhere(Node.board_status == -4))
        #     player2_score = len(np.argwhere(Node.board_status == 4))
        #     return player2_score - player1_score
        
        for i in range (3):
            for j in range (4):
                if Node.Current.row_status[j,i] == 0 and (i,j,"row") not in Node.Positions:
                    Node.Make(i, j, "row", self.player1_turn)
                    # print("row", i, j)

        for i in range (4):
            for j in range (3):
                if Node.Current.col_status[j,i] == 0 and (i,j,"col") not in Node.Positions:
                    Node.Make(i, j, "col", self.player1_turn)
                    # print("col", i, j)
                    
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
                