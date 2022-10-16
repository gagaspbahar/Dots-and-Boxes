from operator import indexOf
from time import time
from Bot import Bot
from GameAction import GameAction
from GameState import GameState
from Nodes import Nodes
import numpy as np

class LocalSearchBot(Bot):
    def __init__(self):
        self.state = GameState()
        self.temperature = 100
        self.temperatureDecrease = 5
        self.chosen_edge_row = [i for i in range(12)]
        self.chosen_edge_col = [i for i in range(12)]

    def simulated_annealing(self, cost_difference, threshold):
        return ans == cost_difference > 0 or np.exp(-cost_difference / self.temperature) >= threshold
    
    def get_action(self) -> GameAction:
        self.player1_turn = state.player1_turn

        return self.get_localsearch_action(self.state)
    
    def objective_func(self, board_status):
        currentScore = 0

        enemy_score = len(argwhere(board_status == -4))
        player_score = len(argwhere(board_status == 4))
        currentScore = 20*(player_score - enemy_score)
        
        if player_score + enemy_score != 9:
            if childState.player1_turn == turn:
                newThreeLine = len(argwhere(abs(board_status) == 3))
                currentScore += 10*(newThreeLine - threeLine)
            else :
                newThreeLine = len(argwhere(abs(board_status) == 3))
                currentScore -= 10*(newThreeLine - threeLine)
        
        return currentScore

    def get_localsearch_action(self,state):
        start = time()

        # --------------- RANDOM SUCCESSOR --------------- 

        currScore = self.objective_func(state)
        succScore = 0
        # Random row / col
        orient = np.random.randint(0,1)
        if orient == 0:
            row = np.random.choice(self.chosen_edge_row)
            self.chosen_edge_row.remove(row)

            # buat state neighbor

            newState = GameState(state.b)


            succScore = self.objective_func(state)






    
        
        
        print("timetaken:", time() - start)
        print("taken: ", rowcol, (i,j))