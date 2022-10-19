from operator import indexOf
from time import time, sleep
from traceback import print_list
from Bot import Bot
from GameAction import GameAction
from GameState import GameState
from numpy import argwhere, random, exp, sum
from copy import deepcopy

class LocalSearchBot(Bot):

    #### INIT
    def __init__(self):
        self.temp = None

    #### GET ACTION
    # Metode yang digunakan untuk mencari tahu aksi yang akan dilakukan oleh bot
    # Return:
    #   GameAction
    def get_action(self, GS: GameState) -> GameAction:
        self.initial_state = GS
        self.chosen_edge_row = set()
        self.chosen_edge_col = set()
        self.player1_turn = GS.player1_turn

        for i in range(3):
            for j in range(4):
                self.chosen_edge_row.add((i,j))
                self.chosen_edge_col.add((j,i))

        self.state = GameState(GS.board_status, GS.row_status, GS.col_status, GS.player1_turn)
        self.player1_turn = self.state.player1_turn
        
        return self.get_localsearch_action(self.state)

    #### OBJECTIVE FUNCTION
    # Metode yang digunakan untuk menghitung nilai dari suatu state
    # Return:
    #   int
    def objective_function(self, board_status):
        currentScore = 0
        playerModifier = 1

        if self.player1_turn:
            playerModifier = -1

        initial_player_score = len(argwhere(self.initial_state.board_status == (4 * playerModifier)))
        enemy_score = len(argwhere(board_status == (-4 * playerModifier)))
        player_score = len(argwhere(board_status == (4 * playerModifier)))
        

        currentScore = 100*(player_score - initial_player_score)
        
        if player_score + enemy_score != 9:
            newThreeLine = len(argwhere(abs(board_status) == 3))
            if (initial_player_score - player_score >= 0):
                currentScore -= 10*(newThreeLine)
            else:
                currentScore += 10*(newThreeLine)
        return currentScore

    #### MOVE
    # Metode yang digunakan untuk menghitung nilai dari suatu state 
    # dengan melakukan perubahan pada state tersebut
    # Return:
    #   int
    def Move(self, i, j, rowcol):
        childState = deepcopy(self.state)
        playerModifier = 1

        if self.player1_turn:
            playerModifier = -1
        
        if j < 3 and i < 3:
            childState.board_status[j][i] = (abs(childState.board_status[j][i]) + 1) * playerModifier

        if rowcol == 'row':
            childState.row_status[j][i] = 1
            if j >= 1:
                childState.board_status[j-1][i] = (abs(childState.board_status[j-1][i]) + 1) * playerModifier

        elif rowcol == 'col':
            childState.col_status[j][i] = 1
            if i >= 1:
                childState.board_status[j][i-1] = (abs(childState.board_status[j][i-1]) + 1) * playerModifier

            
        return self.objective_function(childState.board_status)

    #### ERASE FIELD BOARD
    # Metode yang digunakan untuk menghapus field yang sudah terisi
    # dari list
    # Return:
    #   None
    def erase_field_board(self):
        for i in range(3) :
            for j in range(4):
                if self.state.row_status[j,i] == 1:
                    self.chosen_edge_row.remove((i, j))

        for i in range(4) :
            for j in range(3) :
                if self.state.col_status[j,i] == 1:
                    self.chosen_edge_col.remove((i,j))

    #### GET LOCAL SEARCH ACTION
    # Metode yang digunakan untuk mencari tahu aksi yang akan diambil
    # dengan mengimplementasikan random restart hill-climbing
    # Return:
    #   GameAction
    def get_localsearch_action(self, state):
        start = time()
        self.erase_field_board()

        currScore = self.objective_function(self.state.board_status)
        chosen_i = 0
        chosen_j = 0
        rowcol = ""
        proceed = False

        for check_i,check_j in self.chosen_edge_row:
            if self.Move(check_i,check_j,"row") > currScore:
                proceed = True
                break
        
        if not proceed:
            for check_i,check_j in self.chosen_edge_col:
                if self.Move(check_i,check_j,"col") > currScore:
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
                    
                    succScore = self.Move(try_i,try_j,"row")
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
                    
                    succScore = self.Move(try_i,try_j,"col")
                    if succScore > currScore:
                        currScore = succScore
                        chosen_i = try_i
                        chosen_j = try_j
                        rowcol = "col"
                        self.chosen_edge_col.remove((try_i,try_j))
                        break

        else:
            worstCurrScore = -1000
            for check_i,check_j in self.chosen_edge_row:
                succScore = self.Move(check_i,check_j,"row")

                if succScore >= worstCurrScore:
                    worstCurrScore = succScore
                    chosen_i = check_i
                    chosen_j = check_j
                    rowcol = "row"
                    if worstCurrScore == currScore:
                        break

            if worstCurrScore != currScore:
                for check_i,check_j in self.chosen_edge_col:
                    succScore = self.Move(check_i,check_j,"col")
                    
                    if succScore >= worstCurrScore:
                        worstCurrScore = succScore
                        chosen_i = check_i
                        chosen_j = check_j
                        rowcol = "col"
                        if worstCurrScore == currScore:
                            break
    
            if rowcol == "row" :
                self.chosen_edge_row.remove((chosen_i,chosen_j))
            else:
                self.chosen_edge_col.remove((chosen_i,chosen_j))

            currScore = worstCurrScore
            
        return GameAction(rowcol, (chosen_i,chosen_j))
