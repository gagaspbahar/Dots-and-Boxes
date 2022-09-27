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

        return self.get_minimax_action(Nodes(state), 24-count)

    def get_minimax_action(Node, Depth):
        for i in range (3):
            for j in range (4):
                if Node.Current.row_status[j,i] == 0 and (i,j,"row") not in Node.children:
                    Node.Make(i, j, "row")
                    if Depth < 2 :
                        return GameAction("row", (i,j))

        for i in range (4):
            for j in range (3):
                if Node.Current.col_status[j,i] == 0 and (i,j,"col") not in Node.children:
                    Node.Make(i, j, "col")
                    if Depth < 2 :
                        return GameAction("col", (i,j))

        Minimum_Score = 1000
        i = 0
        j = 0
        rowcol = ""
        for k, z in Nodes.children.items():
            Result = MinimaxBot.Maximum(z, Depth - 1, Minimum_Score)
            if Minimum_Score > Result:
                Minimum_Score = Result
                i = k[0]
                j = k[1]
                rowcol = k[2]

        return GameAction(rowcol, (i,j))

    def Maximum(Node, Depth, Alpha):
        if Depth == 0:
            return Node.CurrentScore
        
        for i in range (3):
            for j in range (4):
                if Node.Current.row_status[j,i] == 0 and (i,j,"row") not in Node.children:
                    Node.Make(i, j, "row")

        for i in range (4):
            for j in range (3):
                if Node.Current.col_status[j,i] == 0 and (i,j,"col") not in Node.children:
                    Node.Make(i, j, "col")

        Maximum_Score = -1000
        for k, z in Nodes.children.items():
            Result = MinimaxBot.Minimum(z, Depth - 1, Maximum_Score)
            if Maximum_Score < Result:
                Maximum_Score = Result
            if Result > Alpha:
                return Result
        
        return Maximum_Score

    def Minimum(Node, Depth, Beta):
        if Depth == 0:
            return Node.CurrentScore
        
        for i in range (3):
            for j in range (4):
                if Node.Current.row_status[j,i] == 0 and (i,j,"row") not in Node.children:
                    Node.Make(i, j, "row")

        for i in range (4):
            for j in range (3):
                if Node.Current.col_status[j,i] == 0 and (i,j,"col") not in Node.children:
                    Node.Make(i, j, "col")

        Minimum_Score = 1000
        for k, z in Nodes.children.items():
            Result = MinimaxBot.Maximum(z, Depth - 1, Minimum_Score)
            if Minimum_Score > Result:
                Minimum_Score = Result
            if Result < Beta:
                return Result
        
        return Minimum_Score
                