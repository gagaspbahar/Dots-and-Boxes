from operator import indexOf
from time import time
from traceback import print_list
from Bot import Bot
from GameAction import GameAction
from GameState import GameState
from numpy import argwhere, random, exp, sum
from copy import deepcopy

class LocalSearchBot(Bot):

    def __init__(self):
        self.temp = None

    def get_action(self, GS: GameState) -> GameAction:
        self.chosen_edge_row = set()
        self.chosen_edge_col = set()

        for i in range(3):
            for j in range(4):
                self.chosen_edge_row.add((i,j))
                self.chosen_edge_col.add((j,i))

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

    def erase_field_board(self):
        for i in range(3) :
            for j in range(4):
                if self.state.row_status[j,i] == 1:
                    self.chosen_edge_row.remove((i, j))

        for i in range(4) :
            for j in range(3) :
                if self.state.col_status[j,i] == 1:
                    self.chosen_edge_col.remove((i,j))
        print("ROW",self.chosen_edge_row)
        print("COL",self.chosen_edge_col)

    def get_localsearch_action(self, state):
        start = time()
        self.erase_field_board()

        currScore = self.objective_function(self.state.board_status)
        del_idx_chosen = 0
        chosen_i = 0
        chosen_j = 0
        rowcol = ""
        proceed = False

        for check_i,check_j in self.chosen_edge_row:
            if self.objective_function(self.Move(check_i,check_j,"row",False).board_status) > currScore:
                proceed = True
                break
        
        if not proceed:
            for check_i,check_j in self.chosen_edge_col:
                if self.objective_function(self.Move(check_i,check_j,"col",False).board_status) > currScore:
                    proceed = True
                    break

        if proceed:
            while True:
                orient = random.randint(0,2)

                if len(self.chosen_edge_row) == 0:
                    orient = 1
                if len(self.chosen_edge_col) == 0:
                    orient = 0
                
                if orient == 0:
                    try_i = random.randint(0,3)
                    try_j = random.randint(0,4)

                    while (try_i , try_j) not in self.chosen_edge_row:
                        try_i = random.randint(0,3)
                        try_j = random.randint(0,4)
                    
                    succScore = self.objective_function(self.Move(try_i,try_j,"row",False).board_status)
                    if succScore > currScore :
                        currScore = succScore
                        chosen_i = try_i
                        chosen_j = try_j
                        rowcol = "row"
                        self.chosen_edge_row.remove((try_i,try_j))
                        break

                else:
                    try_i = random.randint(0,4)
                    try_j = random.randint(0,3)

                    while (try_i , try_j) not in self.chosen_edge_col:
                        try_i = random.randint(0,4)
                        try_j = random.randint(0,3)
                    
                    succScore = self.objective_function(self.Move(try_i,try_j,"col",False).board_status)
                    if succScore > currScore:
                        currScore = succScore
                        chosen_i = try_i
                        chosen_j = try_j
                        rowcol = "col"
                        self.chosen_edge_col.remove((try_i,try_j))
                        break
        else:
            orient = random.randint(0,2)
            if len(self.chosen_edge_row) == 0:
                orient = 1
            if len(self.chosen_edge_col) == 0:
                orient = 0
            
            if orient == 0:
                idx_chosen = random.randint(0,len(self.chosen_edge_row))
                chosen_i = (list(self.chosen_edge_row))[idx_chosen][0]
                chosen_j = (list(self.chosen_edge_row))[idx_chosen][1]
                rowcol = "row"
            else:
                idx_chosen = random.randint(0,len(self.chosen_edge_col))
                chosen_i = (list(self.chosen_edge_col))[idx_chosen][0]
                chosen_j = (list(self.chosen_edge_col))[idx_chosen][1]
                rowcol = "col"
            
        print("\ncurrscore akhir :", currScore)
        print("timetaken:", time() - start)
        print("taken: ", rowcol, (chosen_i,chosen_j))
        return GameAction(rowcol, (chosen_i,chosen_j))
