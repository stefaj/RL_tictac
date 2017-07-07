from __future__ import print_function
import numpy as np
from scipy import stats
import random
import matplotlib.pyplot as plt
import random
import pickle
import time
import os.path
# %matplotlib inline


def printBoard(grid):
    for i in range(0,3):
        for j in range(0,3):
            print('|' + grid[i*3+j], end='')
        print('|\n-------')

def play(grid, player, i, j):
    grid[i*3+j] = 'o' if player == 0 else 'x'
    return grid

def hasThreeInRow(grid, player):
    p = 'o' if player == 0 else 'x'
    return ((grid[0] == grid[1] == grid[2] == p) or
           (grid[3] == grid[4] == grid[5] == p) or
           (grid[6] == grid[7] == grid[8] == p) or
           (grid[0] == grid[3] == grid[6] == p) or
           (grid[1] == grid[4] == grid[7] == p) or
           (grid[2] == grid[5] == grid[8] == p) or
           (grid[0] == grid[4] == grid[8] == p) or
           (grid[2] == grid[4] == grid[6] == p))


class HumanPlayer:
    ident = 0
    def __init__(self, identifier):
        self.ident = identifier
    def get_move(self, grid):
        try:
            return int(raw_input('Enter your move player ' + str(self.ident) + ':'))
        except:
            return self.get_move(grid)

class RLQLearner:
    Q_cache = {}
    alpha = 0.3
    gamma = 0.9
    epsilon = 0.8
    player_index = 0

    def __init__(self, player_index, learning_rate, discount_factor, epsilon,
            Q_cache={}):
        self.alpha = learning_rate 
        self.player_index = player_index
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.Q_cache = Q_cache

    def hash_list(self, l):
        h = 0
        for i in range(0,9):
            num = 0
            if l[i] == 'o':
                num = 1
            if l[i] == 'x':
                num = 2
            h += num * 7^i 
        return h

        
    def get_q(self, grid, action):
        if self.get_reward(grid) != 0:
            return self.get_reward(grid)
        if not (self.hash_list(grid), action) in self.Q_cache:
            self.Q_cache[(self.hash_list(grid), action)] = 0
        return self.Q_cache[(self.hash_list(grid), action)]
    
    def get_reward(self, grid):
        if hasThreeInRow(grid, self.player_index):
            return 10
        elif hasThreeInRow(grid, 1-self.player_index):
            return -10
        elif len( [0 for i in range(0,9) if grid[i] == ' '] ) == 0:
            return 5
        else:
            return 0

    def update_q(self, grid, action):
        old_val = self.get_q(grid, action)
        reward = self.get_reward(grid)

        new_grid = grid[:]
        new_grid[action] = 'o' if self.player_index == 0 else 'x'
        best_estimate = max( [ self.get_q(new_grid, a) for a in range(0,9) ] )

        new_val = old_val + self.alpha*(reward + self.gamma*best_estimate -
                old_val)
        self.Q_cache[(self.hash_list(grid),action)] = new_val

    def get_best_action(self, grid):
        ba = random.choice( [i for i in range(0,9) if grid[i] == ' '] )
        m = -100000.0
        for a in range(0,9):
            if self.get_q(grid, a) > m and grid[a] == ' ':
                m = self.get_q(grid, a)
                ba = a
        return ba

    def get_action(self, grid): # Greedy epsilon
        print('eps', self.epsilon)
        if np.random.rand() < self.epsilon: # uniform
            return random.choice( [i for i in range(0,9) if grid[i] == ' '] )
        else: # best 1-eps
            print('taking best move..')
            return self.get_best_action(grid)

    def get_move(self, grid):
        action = self.get_action(grid)
        self.update_q(grid, action)
        # if self.epsilon > 0.01:
        #     self.epsilon *= 0.99999
        return action 

def main():
    grid = [' ']*9
    player1 = HumanPlayer(1)
    # player1 = RLQLearner(0, 0.3, 0.9, 0.8)
    player2 = RLQLearner(1, 0.3, 0.9, 0.8)


    if os.path.isfile('player1.p') and not (isinstance(player1, HumanPlayer)):
        print('Loading player1 from file')
        player1 = pickle.load( open( "player1.p", "rb" ) )
    if os.path.isfile('player2.p'):
        print('Loading player2 from file')
        player2 = pickle.load( open( "player2.p", "rb" ) )

    if isinstance(player1, HumanPlayer):
        player2.epsilon = 0
        print(player2.Q_cache)

    while True:
        printBoard(grid)
        for turn in range(0,8):
            print('')

            p1move = -1 # Player one move
            while p1move == -1:
                p1move = player1.get_move(grid)
                if grid[p1move] != ' ':
                    p1move = -1
            grid = play(grid, 0, p1move // 3, p1move % 3)
            printBoard(grid)
            if hasThreeInRow(grid, 0): # player 1 won
                print('Player 1 won')
                break
            if len([0 for i in range(0,9) if grid[i] == ' ']) == 0:
                break # failsafe

            print('')

            p2move = -1 # Player one move
            while p2move == -1:
                p2move = player2.get_move(grid)
                if grid[p2move] != ' ':
                    p2move = -1
            grid = play(grid, 1, p2move // 3, p2move % 3)
            printBoard(grid)
            if hasThreeInRow(grid, 1): # player 1 won
                print('Player 2 won')
                break
            # time.sleep(5.0)

        pickle.dump( player1, open( "player1.p", "wb" ) )
        pickle.dump( player2, open( "player2.p", "wb" ) )

        print("Starting next round in 1s...")
        # time.sleep(1.0)
        grid = [' ']*9
   
random.seed()
main()

