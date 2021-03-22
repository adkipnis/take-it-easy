#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Take it easy
"""
import itertools as it
import numpy as np

class TIE():
# Initialization    
    def __init__(self):
        # Fields
        field_full = np.array([(i,j) for i in range(5) for j in range(5)])
        empty_idx = [3, 4, 9, 19, 23, 24]
        self.field_orig = np.delete(field_full, empty_idx, axis = 0)
        self.field = self.field_orig.copy()
        
        # Diagonals
        self.diag_r = [self.field[self.field[:,0] == i] for i in range(5)]
        self.diag_l = [self.field[self.field[:,1] == i] for i in range(5)]
        
        # Columns
        c_1 = np.array([[i,0] for i in range(2,5)])
        c_2 = np.concatenate(([[1,0]], [[i,1] for i in range(2,5)]))
        c_3 = np.concatenate(([[i,i] for i in range(3)], [[3,2], [4,2]]))
        c_4 = np.array([[0+i,1+i] for i in range(4)])
        c_5 = np.array([[0+i,3+i] for i in range(3)])
        self.cols = [c_1, c_2, c_3, c_4, c_5]
        
        # Cards
        set_u = {1,5,9}
        set_l = {2,6,7}
        set_r = {3,4,8}
        self.deck = np.array([(i) for i in it.product(set_u, set_l, set_r)])
        
        # Rest
        self.limbo = []
        self.placed = []
        self.score = 0
        
# Basic Actions
    def draw_card(self):
        if len(self.limbo) == 0:
            choice_idx = np.random.choice(len(self.deck), 1)
            self.limbo = self.deck[choice_idx]
            self.show_drawn()
            self.deck = np.delete(self.deck, choice_idx, axis = 0)
        else:
            print("You must first place your drawn card")
    
    def random_pos(self):
        choice_idx = np.random.choice(len(self.field), 1)
        return self.field[choice_idx]
        
    def place_card(self, pos = None):
        assert len(self.field) > 0, "No more cards to draw."
        if pos is None:
            pos = self.random_pos()
        print("Position:", pos[0])
        if pos in self.field:
            self.field = np.delete(
                self.field,
                np.argwhere(np.all(pos == self.field, axis = 1)),
                axis=0)
            self.placed.append((self.limbo[0], pos[0]))
            self.limbo = []
        else:
            print("The chosen position is not available.")
    
    def single_round(self, pos = None):
        self.draw_card()
        self.place_card(pos = pos)
    
    def random_game(self):
        while len(self.field) > 0:
            self.single_round()

# Evaluation   
    def eval_streak(self, bar, number_idx):
        bar_score = 0
        for col in bar:
            streak = []
            for turn in self.placed:
                if np.any(np.all(turn[1] == col, axis = 1)):
                    streak.append(turn[0][number_idx])
            if len(np.unique(streak)) == 1:
                bar_score += np.sum(streak)
        print("Points:", bar_score) 
        self.score += bar_score
         
    def eval_score(self):
        self.eval_streak(self.cols, 0)
        self.eval_streak(self.diag_l, 1)
        self.eval_streak(self.diag_r, 2)
        print("Points total:", self.score) 

# Getter functioins      
    def show_deck(self):
        return self.deck.copy()
    
    def show_drawn(self):
        if len(self.limbo)>0:
            print("Card:", self.limbo[0])
            
##############################################################################

game = TIE()
game.show_deck()
game.random_game()
game.eval_score()