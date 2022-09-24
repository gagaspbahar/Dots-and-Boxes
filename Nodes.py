from GameState import GameState

class Nodes(GameState):
    def __init__(self, GameState):
        self.Current = GameState
        self.CurrentScore = 0
        self.children = {}
    
    def Make(self, i, j, rowcol):
        childState = self.Current
        childState.board_status[j,i] = 1
        if rowcol == "row":
            childState.row_status[j,i] = 1
        else:
            childState.col_status[j,i] = 1
        childState.player1_turn = not childState.player1_turn

        self.children[(i, j, rowcol)] = Nodes(childState)
        
    def Populate(self, i, j, Child):
        self.children[(i,j)] = Child