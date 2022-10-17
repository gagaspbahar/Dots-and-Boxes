from operator import indexOf
from time import time
from Bot import Bot
from GameAction import GameAction
from GameState import GameState
from numpy import argwhere, random, exp
from copy import deepcopy

class LocalSearchBot(Bot):

    def __init__(self):
        self.temp = None

    def get_action(self, GS: GameState) -> GameAction:
        self.chosen_edge_row = [i for i in range(12)]
        self.chosen_edge_col = [i for i in range(12)]

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

            
        return GameState(childState.board_status, childState.row_status, childState.col_status, childState.player1_turn if pointScored else not childState.player1_turn)

    def get_localsearch_action(self, state):
        start = time()
        print("START")

        # currScore = self.objective_function(state.board_status)
        currScore = -1000
        del_idx_chosen = 0
        chosen_i = 0
        chosen_j = 0

        rowcol = ""
        print("currScore awal : ", currScore)

        for row in self.chosen_edge_row :
            i, j  = row % 3 , row // 3
            if state.row_status[j][i] == 1:
                self.chosen_edge_col.remove(row)
                continue
            succScore = self.objective_function(self.Move(i,j,"row",False).board_status)
            print("succscore || row || ", i ," ", j," :",  succScore)
            if succScore > currScore:
                currScore = succScore
                del_idx_chosen = row
                chosen_i = i
                chosen_j = j
                rowcol = "row"
                print("succscore terpilih || ", rowcol ," || ",chosen_i," ",chosen_j," :",  succScore)


        for col in self.chosen_edge_col :
            i, j  = col % 4 , col // 4
            if state.col_status[j][i] == 1:
                self.chosen_edge_col.remove(col)
                continue

            succScore = self.objective_function(self.Move(i,j,"col",False).board_status)
            print("succscore || col || ", i ," ", j," :",  succScore)
            if succScore > currScore:
                currScore = succScore
                del_idx_chosen = col
                chosen_i = i
                chosen_j = j
                rowcol = "col"
                print("succscore terpilih || ", rowcol ," || ",chosen_i," ",chosen_j," :",  succScore)

        if rowcol == "row":
            self.chosen_edge_row.remove(del_idx_chosen)
        else:
            self.chosen_edge_col.remove(del_idx_chosen)

        print("currscore akhir :", currScore)
        print("timetaken:", time() - start)
        print("taken: ", rowcol, (chosen_i,chosen_j))
        return GameAction(rowcol, (chosen_i,chosen_j))
