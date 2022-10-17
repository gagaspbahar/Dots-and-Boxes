from operator import indexOf
from time import time
from Bot import Bot
from GameAction import GameAction
from GameState import GameState
from numpy import argwhere, random, exp
from copy import deepcopy

class LocalSearchBot(Bot):

    def get_action(self, GS: GameState) -> GameAction:
        self.state = GameState(GS.board_status, GS.row_status, GS.col_status, GS.player1_turn)
        self.player1_turn = self.state.player1_turn
        
        return self.get_localsearch_action(self.state)

    def objective_function(self, board_status):
        currentScore = 0

        enemy_score = len(argwhere(board_status == -4))
        player_score = len(argwhere(board_status == 4))
        currentScore = 20*(player_score - enemy_score)
        
        if player_score + enemy_score != 9:
            newThreeLine = len(argwhere(abs(board_status) == 3))
            currentScore -= 10*(newThreeLine)
        
        return currentScore

    def Move(self, i, j, rowcol, turn):
        childState = deepcopy(self.state)
        playerModifier = 1
        pointScored = False
        nextTurn = True

        if childState.player1_turn != turn:
            playerModifier = -1
        
        if j < 3 and i < 3:
            childState.board_status[j][i] = (abs(childState.board_status[j][i]) + 1) * playerModifier
            if abs(childState.board_status[j][i]) == 4:
                pointScored = True

        if rowcol == 'row':
            childState.row_status[j][i] = 1
            if j >= 1:
                childState.board_status[j-1][i] = (abs(childState.board_status[j-1][i]) + 1) * playerModifier
                if abs(childState.board_status[j-1][i]) == 4:
                    pointScored = True

        elif rowcol == 'col':
            childState.col_status[j][i] = 1
            if i >= 1:
                childState.board_status[j][i-1] = (abs(childState.board_status[j][i-1]) + 1) * playerModifier
                if abs(childState.board_status[j][i-1]) == 4:
                    pointScored = True

        # P yg ini AttributeError: kant set attirbtutvc
            
        # return childState
        return GameState(childState.board_status, childState.row_status, childState.col_status, childState.player1_turn if pointScored else not childState.player1_turn)

    def get_localsearch_action(self, state):
        start = time()
        print("START")
        currScore = self.objective_function(state.board_status)
        k = 0
        l = 0
        rowcol = ""
        print("currScore awal : ", currScore)

        # Loop semua neighbor state
        for i in range (3):
            for j in range (4):
                if state.row_status[j,i] == 0 and (i,j,"row") :
                    succScore = self.objective_function(self.Move(i,j,"row",self.player1_turn).board_status)
                    if succScore > currScore:
                        currScore = succScore
                        k = i
                        l = j
                        rowcol = "row"
                        print("succscore (",k," ",l," :",  succScore)
        
        for i in range (4):
            for j in range (3):
                if state.col_status[j,i] == 0 and (i,j,"col"):
                    succScore = self.objective_function(self.Move(i,j,"col",self.player1_turn).board_status)
                    if succScore > currScore:
                        currScore = succScore
                        k = i
                        l = j
                        rowcol = "col"
                        print("succscore (",k," ",l," :",  succScore)

        print("timetaken:", time() - start)
        print("taken: ", 'row', (k,l))
        return GameAction(rowcol, (k,l))
