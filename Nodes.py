from GameState import GameState
import numpy as np

class Nodes(GameState):
    def __init__(self, GameState):
        self.Current = GameState
        self.CurrentScore = 0
        self.children = {}

    def update_board(self, x, y, type):
        val = 1
        playerModifier = 1
        pointScored = False
        if self.player1_turn:
            playerModifier = -1
            

        if y < 3 and x < 3:
            self.board_status[y][x] = (abs(self.board_status[y][x]) + val) * playerModifier
            if abs(self.board_status[y][x]) == 4:
                pointScored = True

        if type == 'row':
            self.row_status[y][x] = 1
            if y >= 1:
                self.board_status[y-1][x] = (abs(self.board_status[y-1][x]) + val) * playerModifier
                if abs(self.board_status[y-1][x]) == 4:
                    pointScored = True

        elif type == 'col':
            self.col_status[y][x] = 1
            if x >= 1:
                self.board_status[y][x-1] = (abs(self.board_status[y][x-1]) + val) * playerModifier
                if abs(self.board_status[y][x-1]) == 4:
                    pointScored = True

        if not pointScored:
            self.player1_turn = not self.player1_turn
    
    def Make(self, i, j, rowcol):
        childState = self.Current
        childState.update_board(i, j, rowcol)

        count = 0
        for i in range (4):
            for j in range (4) :
                if childState.row_status[j,i] == 1:
                    count += 1
                if childState.col_status[j,i] == 1:
                    count += 1
        if count == 24:
            player1_score = len(np.argwhere(self.board_status == -4))
            player2_score = len(np.argwhere(self.board_status == 4))
            childState.CurrentScore = player2_score - player1_score

        self.children[(i, j, rowcol)] = Nodes(childState)
        
    def Populate(self, i, j, rowcol, Child):
        self.children[(i,j,rowcol)] = Child