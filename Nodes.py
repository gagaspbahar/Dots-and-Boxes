from GameState import GameState
from copy import deepcopy
import numpy as np

class Nodes(GameState):
    def __init__(self, board_status, row_status, col_status, player1_turn):
        self.Current = GameState(board_status, row_status, col_status, player1_turn)
        self.CurrentScore = 0
        self.Children = {}
        
    
    def Make(self, i, j, rowcol, temp):
        childState = deepcopy(self.Current)
        val = 1
        playerModifier = 1
        pointScored = False
        nextTurn = True
        currentScore = 0
        threeLine = len(np.argwhere(abs(self.board_status) == 3))
        if childState.player1_turn:
            playerModifier = -1
        
        if j < 3 and i < 3:
            childState.board_status[j][i] = (abs(childState.board_status[j][i]) + val) * playerModifier
            if abs(childState.board_status[j][i]) == 4:
                pointScored = True

        if rowcol == 'row':
            childState.row_status[j][i] = 1
            if j >= 1:
                childState.board_status[j-1][i] = (abs(childState.board_status[j-1][i]) + val) * playerModifier
                if abs(childState.board_status[j-1][i]) == 4:
                    pointScored = True

        elif rowcol == 'col':
            childState.col_status[j][i] = 1
            if i >= 1:
                childState.board_status[j][i-1] = (abs(childState.board_status[j][i-1]) + val) * playerModifier
                if abs(childState.board_status[j][i-1]) == 4:
                    pointScored = True

        if not pointScored:
            nextTurn = not childState.player1_turn
        else:
            nextTurn = childState.player1_turn
        

        count = 0
        for x in range (3):
            for y in range (4) :
                if childState.row_status[y,x] == 1:
                    count += 1
        for x in range (4):
            for y in range (3) :
                if childState.col_status[y,x] == 1:
                    count += 1

        if count == 24:
            player1_score = len(np.argwhere(self.board_status == -4))
            player2_score = len(np.argwhere(self.board_status == 4))
            currentScore = player2_score - player1_score

        elif childState.player1_turn:
            player1_score = len(np.argwhere(self.board_status == -4))
            player2_score = len(np.argwhere(self.board_status == 4))
            newThreeLine = len(np.argwhere(abs(self.board_status) == 3))
            currentScore = player2_score - player1_score
            if newThreeLine > threeLine:
                currentScore += 10
            if newThreeLine < threeLine:
                currentScore -= 10

        else :
            player1_score = len(np.argwhere(self.board_status == -4))
            player2_score = len(np.argwhere(self.board_status == 4))
            newThreeLine = len(np.argwhere(abs(self.board_status) == 3))
            currentScore = player2_score - player1_score
            if newThreeLine > threeLine:
                currentScore -= 10
            if newThreeLine < threeLine:
                currentScore += 10

        self.Children[(i, j, rowcol)] = Nodes(childState.board_status, childState.row_status, childState.col_status, nextTurn)
        self.Children[(i, j, rowcol)].CurrentScore = currentScore
        
    def Populate(self, i, j, rowcol, Child):
        self.Children[(i,j,rowcol)] = Child