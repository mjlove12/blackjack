import math
import random
from cards import Card, Hand, Deck
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

'''
NEXT STEPS:
Refine Rules:
    Deal with Aces
    When to exchange the deck
    Splitting
Add Betting
Add Splitting
Add Different Strategies and Compare Outcomes
    Simulate Card Counting
'''

class Mtrx(object):
    '''Dictionary of Ratios
    Player uses as a guide to decide whether to hit or not for each scenario

    Attributes:
        hits: dictionary of every time a player should have hits
        scenarios: dictionary of every score combination encountered
        ratios: dictionary with ratio of hits to scenarios
                can be used as a probability for deciding to hit or stay'''
    def __init__(self):
        self.hits = dict()
        self.scenarios = dict()
        self.ratios = dict()
        player_values = range(4,22) #player only has values 4 - 22
        dealer_values = range(2,12) #dealer only has values 2 to 11
        for i in player_values:
            for j in dealer_values:
                self.scenarios[i, j] = 0.0
                self.hits[i, j] = 0.0
                self.ratios[i, j] = 0.0

    def update_hits(self, key):
        '''Updates the hit matrix. Should be used every
        time the player should have hit.'''
        self.hits[key] += 1
        if self.scenarios[key] == 0.0:
            self.ratios[key] = 0.0
        else:
            self.ratios[key] = self.hits[key] / self.scenarios[key]
        return(self)

    def update_scenarios(self, key):
        '''Updates the hit matrix. Should be used every
        time the player should have hit.'''
        self.scenarios[key] += 1
        if self.scenarios[key] == 0.0:
            self.ratios[key] = 0.0
        else:
            self.ratios[key] = self.hits[key] / self.scenarios[key]
        return(self)


def decide(player, dealer, mtrx):
    '''Takes the players hand, dealers hand, decision matrix
    and returns a decision to hit or stay'''
    score = (player.tally(), dealer.tally())
    if mtrx.scenarios[score] == 0:
        #Randomly choose hit or stay
        x = random.randint(0,1)
        if x == 1:
            return 1 #HIT!
        else:
            return 0 #STAY!
    else:
        #Use past ratios of good to total outcomes
        x = random.uniform(0.0,1.0)
        if x < mtrx.ratios[score]:
            return 1 #HIT!
        else:
            return 0 #STAY


def play_round(mtrx, deck):
    player = Hand()
    dealer = Hand()

    deck.deal(player, 2)
    deck.deal(dealer, 1)

    decision = 1

    '''Takes the players hand, dealers hand and decision matrix
    and returns the revised player hand'''
    while(decision == 1 and player.tally() < 21):
        #Assess the score, decide whether to hit or stay
        score = (player.tally(), dealer.tally()) #Evaluate score
        mtrx.update_scenarios(score) #Log the instance
        #print("SCENARIO UPDATE")
        decision = decide(player, dealer, mtrx) #Decide hit or stay
        if decision == 0:
            break #Decided to stay, leave loop
        else:
            #Decided to leave and log successful hit if still under 21
            deck.deal(player, 1)
            if player.tally() < 21:
                #print("PLAYER HIT ON " + str(score))
                #print("PLAYER NOW HAS " + str(player.tally()))
                mtrx.update_hits(score) #Successful hit
                #print("SUCCESS: HIT UPDATE")

    '''3 ways to leave the loop:
        1. HIT & bust
        2. HIT & get 21
        3. STAY'''

    #Dealer Turn
    #What does the dealer do if he's already beating the player?
    #Does he still play to 17?
    while dealer.tally() < 17:
        deck.deal(dealer,1)

    if player.tally() > 21:
        outcome = 0 #Bust, player loses

    elif dealer.tally() > 21:
        outcome = 1 #Dealer bust, player wins!

    elif dealer.tally() > player.tally():
        outcome = 0 #Dealer Wins!

    elif dealer.tally() == player.tally():
        outcome = 2 #Tie!

    else:
        outcome = 1 #Player Wins!

    if outcome == 0 and decision == 0:
        #print("PLAYER STAYED ON "+str(score))
        mtrx.update_hits(score)
        score = (player.tally(), dealer.tally())
        #print("PLAYER NOW HAS "+str(score))
        #print("SHOULD HAVE HIT: HIT UPDATE")
