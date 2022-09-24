from Bot import Bot
from GameAction import GameAction
from GameState import GameState
from Nodes import Nodes

class MinimaxBot(Bot):
    def get_action(self, state: GameState) -> GameAction:
        pass

    def get_minimax_action(Node, Depth):
        for i in range (4):
            for j in range (4):
                if Node.Current.row_status[j,i] == 0 and (i,j) not in Node.children:
                    Node.Make(i, j, "row")
                    if Depth < 2 :
                        return GameAction("row", (i,j))
                if Node.Current.col_status[j,i] == 0 and (i,j) not in Node.children:
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
        pass

    def Minimum(Node, Depth, Beta):
        pass
                