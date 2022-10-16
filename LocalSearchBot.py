from operator import indexOf
from time import time
from Bot import Bot
from GameAction import GameAction
from GameState import GameState
from numpy import argwhere, random, exp
from copy import deepcopy

class LocalSearchBot(Bot):
    
    def __init__(self):
        # TODO reset temperature
        self.temperature = 100
        self.temperatureDecrease = 5

    def get_action(self, GS: GameState) -> GameAction:
        self.chosen_edge_row = [i for i in range(12)]
        self.chosen_edge_col = [i for i in range(12)]
        self.state = GameState(GS.board_status, GS.row_status, GS.col_status, GS.player1_turn)
        self.player1_turn = self.state.player1_turn
        
        return self.get_localsearch_action(self.state)

    def simulated_annealing(self, cost_difference, threshold):
        return cost_difference > 0 or exp(-cost_difference / self.temperature) >= threshold

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
        succScore = 0

        orient = random.randint(0,2)
        success = False

        print("orient :",orient)
        if 0 not in state.row_status:
            orient = 1
        if 0 not in state.col_status:
            orient = 0

        if orient == 0:

            # TODO : Randomize nya diatur, biar ga random hal yang saa lagi
            while not success:
                print(self.chosen_edge_row)
                chosen_row = random.choice(self.chosen_edge_row)
                i,j = chosen_row % 3 , chosen_row // 3
                if state.row_status[j][i] == 1:
                    self.chosen_edge_row.remove(chosen_row)
                    continue
                neighborState = self.Move(i,j ,'row', False) # TODO : False placeholder dulu
                succScore = self.objective_function(neighborState.board_status)
                success = self.simulated_annealing(succScore - currScore, 0.5)

                if success :
                    self.state = neighborState
                    # self.chosen_edge_row.remove(chosen_row)

                    # TODO : T turunin gmn
                    self.temperature -= self.temperatureDecrease

                    print(self.chosen_edge_row)
                    print("timetaken:", time() - start)
                    print("taken: ", 'row', (i,j))
                    return GameAction('row', (i,j))
            
        else:        
            while not success:
                chosen_col = random.choice(self.chosen_edge_col)
                i,j = chosen_col % 4 , chosen_col // 4
                if state.col_status[j][i] == 1:
                    self.chosen_edge_col.remove(chosen_col)
                    continue
                neighborState = self.Move(i,j,'col', False) # TODO : False placeholder dulu
                succScore = self.objective_function(neighborState.board_status)
                success = self.simulated_annealing(succScore - currScore, 0.5)

                if success : 
                    self.state = neighborState
                    # self.chosen_edge_col.remove(chosen_col)

                    # TODO : T turunin gmn
                    self.temperature -= self.temperatureDecrease

                    print(self.chosen_edge_col)
                    print("timetaken:", time() - start)
                    print("taken: ", 'col', (i,j))
                    return GameAction('col',(i,j))

