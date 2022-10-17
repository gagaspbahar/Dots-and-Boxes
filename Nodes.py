import heapq
from GameState import GameState
from copy import deepcopy
from numpy import argwhere

class Nodes():
    def __init__(self, board_status, row_status, col_status, player1_turn, minimax = True, currentScore = 0, position = (0,0,""), scoreWithThreeline = 0):
        self.Current = GameState(board_status, row_status, col_status, player1_turn)
        self.Positions = []
        self.Position = position
        self.Minimax = minimax
        self.CurrentScore = currentScore
        self.ScoreWithThreeline = scoreWithThreeline
        self.Children = []
        heapq.heapify(self.Children)
    
    def __lt__(self, other):
        return self.ScoreWithThreeline > other.ScoreWithThreeline
        # if not self.Minimax:
        #     return self.ScoreWithThreeline < other.ScoreWithThreeline
        # else:
        #     return self.ScoreWithThreeline > other.ScoreWithThreeline
    
    def Make(self, i, j, rowcol, myTurn):
        childState = deepcopy(self.Current)
        playerModifier = 1
        pointScored = False
        nextTurn = not myTurn
        currentScore = 0
        scoreWithThreeLine = 0
        threeLine = len(argwhere(abs(self.Current.board_status) == 3))
        if childState.player1_turn != myTurn:
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

        if not pointScored:
            nextTurn = not childState.player1_turn
        else:
            nextTurn = childState.player1_turn
        

        # count = 0
        # for x in range (3):
        #     for y in range (4) :
        #         if childState.row_status[y,x] == 1:
        #             count += 1
        # for x in range (4):
        #     for y in range (3) :
        #         if childState.col_status[y,x] == 1:
        #             count += 1

        # TURN = FALSE
        # if minimaxBot == player2 -> TURN = FALSE
        # if minimaxBot == player1 -> TURN = TRUE
        # if not myTurn:
        #     # if minimax bot player2
        #     initial_player_score = len(argwhere(self.Current.board_status == 4))
        #     enemy_score = len(argwhere(childState.board_status == -4))
        #     player_score = len(argwhere(childState.board_status == 4))
            
        # else:
        #     # if minimax bot player1
        #     initial_player_score = len(argwhere(self.Current.board_status == -4))
        #     enemy_score = len(argwhere(childState.board_status == 4))
        #     player_score = len(argwhere(childState.board_status == -4))

        # if minimax bot player2
        initial_player_score = len(argwhere(self.Current.board_status == 4))
        enemy_score = len(argwhere(childState.board_status == -4))
        player_score = len(argwhere(childState.board_status == 4))


        currentScore = 20*(player_score - enemy_score)

        delta_player_score = player_score - initial_player_score


        

        if childState.player1_turn != myTurn:
            newThreeLine = len(argwhere(abs(childState.board_status) == 3))
            scoreWithThreeLine = delta_player_score * 40 + 10*(newThreeLine - threeLine)
        else :
            newThreeLine = len(argwhere(abs(childState.board_status) == 3))
            scoreWithThreeLine = delta_player_score * 40 - 10*(newThreeLine - threeLine)

        # self.Children[self.encode(i,j,rowcol)] = Nodes(childState.board_status, childState.row_status, childState.col_status, nextTurn)
        # self.Children[self.encode(i, j, rowcol)].CurrentScore = currentScore
        # (pq_score, (i,j,rowcol))
        # (pq_score, Nodes)
        # self.Children.append(Nodes(childState.board_status, childState.row_status, childState.col_status, nextTurn, currentScore, (i,j,rowcol)))
        if nextTurn:
            heapq.heappush(self.Children, Nodes(childState.board_status, childState.row_status, childState.col_status, nextTurn, self.Minimax, currentScore, (i,j,rowcol), scoreWithThreeLine))
        else:
            heapq.heappush(self.Children, Nodes(childState.board_status, childState.row_status, childState.col_status, nextTurn, not self.Minimax, currentScore, (i,j,rowcol), scoreWithThreeLine))
        self.Positions.append((i,j,rowcol))

    # def Populate(self, i, j, rowcol, Child):
    #     self.Children[self.encode(i,j,rowcol)] = Child