from Bot import Bot
from GameAction import GameAction
from GameState import GameState
from Nodes import Nodes

class MinimaxBot(Bot):
    def get_action(self, state: GameState) -> GameAction:
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
        # print(count)
        # print(state.board_status)
        # print(state.row_status)
        # print(state.col_status)
        # print(state.player1_turn)
        # State = GameState(state.board_status, state.row_status, state.col_status, state.player1_turn)
        Node = Nodes(state.board_status, state.row_status, state.col_status, state.player1_turn)
        return self.get_minimax_action(Node, count)

    def get_minimax_action(self, Node, Depth):
        for i in range (3):
            for j in range (4):
                if Node.Current.row_status[j,i] == 0 and (i,j,"row") not in Node.Children:
                    Node.Make(i, j, "row")
                    # print("row", i, j)
                    # print(Node.Children[(i, j, "row")])
                    if Depth < 2 :
                        return GameAction("row", (i,j))

        for i in range (4):
            for j in range (3):
                if Node.Current.col_status[j,i] == 0 and (i,j,"col") not in Node.Children:
                    Node.Make(i, j, "col")
                    # print("col", i, j)
                    # print(Node.Children[(i, j, "col")])
                    if Depth < 2 :
                        return GameAction("col", (i,j))

        Minimum_Score = 1000
        i = 0
        j = 0
        rowcol = ""
        for k, z in Node.Children.items():
            Result = self.Maximum(z, Depth - 1, Minimum_Score)
            # print(k)
            # print(Result)
            if Minimum_Score > Result:
                Minimum_Score = Result
                i = k[0]
                j = k[1]
                rowcol = k[2]

        print(rowcol, (i,j))
        return GameAction(rowcol, (i,j))

    def Maximum(self, Node, Depth, Alpha):
        # print(Depth)
        if Depth == 0:
            # print(Node.CurrentScore)
            return Node.CurrentScore
        
        for i in range (3):
            for j in range (4):
                if Node.Current.row_status[j,i] == 0 and (i,j,"row") not in Node.Children:
                    Node.Make(i, j, "row")
                    # print("row", i, j)

        for i in range (4):
            for j in range (3):
                if Node.Current.col_status[j,i] == 0 and (i,j,"col") not in Node.Children:
                    Node.Make(i, j, "col")
                    # print("col", i, j)

        Maximum_Score = -1000
        # print(Node.Children)
        for k, z in Node.Children.items():
            Result = self.Minimum(z, Depth - 1, Maximum_Score)
            # print(k)
            # print(Result)
            if Maximum_Score < Result:
                Maximum_Score = Result
            if Result > Alpha:
                return Result
        
        return Maximum_Score

    def Minimum(self, Node, Depth, Beta):
        # print(Depth)
        if Depth == 0:
            # print(Node.CurrentScore)
            return Node.CurrentScore
        
        for i in range (3):
            for j in range (4):
                if Node.Current.row_status[j,i] == 0 and (i,j,"row") not in Node.Children:
                    Node.Make(i, j, "row")
                    # print("row", i, j)

        for i in range (4):
            for j in range (3):
                if Node.Current.col_status[j,i] == 0 and (i,j,"col") not in Node.Children:
                    Node.Make(i, j, "col")
                    # print("col", i, j)

        Minimum_Score = 1000
        for k, z in Node.Children.items():
            Result = self.Maximum(z, Depth - 1, Minimum_Score)
            # print(k)
            # print(Result)
            if Minimum_Score > Result:
                Minimum_Score = Result
            if Result < Beta:
                return Result
        
        return Minimum_Score
                