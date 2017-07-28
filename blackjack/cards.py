"""This module contains code from
Think Python by Allen B. Downey
http://thinkpython.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

Modified slightly to accomodate blackjack
"""


import math
import random

class Card(object):
    '''Represents a standard playing card

    Attributes:
        suit: integer 0-3
        rank: integer 1-11 (varies by game)
    '''

    suit_names = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    rank_names = [None, 'Ace', '2', '3', '4', '5', '6', '7',
              '8', '9', '10', 'Jack', 'Queen', 'King']

    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank

        #Ranking specific to blackjack
        if rank >= 10:
            self.value = 10

        elif rank == 1:
            self.value = 11

        else:
            self.value = self.rank

    def __str__(self):
        '''Returns human readable string representation'''
        return '%s of %s' % (Card.rank_names[self.rank],
                             Card.suit_names[self.suit])

    def __cmp__(self, other):
        '''Compares two cards by rank'''
        if self.rank > other.rank:
            return 1

        elif self.rank < other.rank:
            return -1

        # ranks are the same... it's a tie
        else:
            return 0

class Hand(object):
    '''Represents a collection of playing cards

    Attributes:
        cards: List of Card objects
    '''

    def __init__(self):
        self.cards = []

    def __str__(self):
        '''Human readable representation
        of collection of cards'''
        res = []
        for card in self.cards:
            res.append(str(card))
        return '\n'.join(res)

    def shuffle(self):
        random.shuffle(self.cards)

    def tally(self):
        tally = 0
        for card in self.cards:
            tally += card.value
        return tally

class Deck(Hand):
    '''Represents a type of hand that is a full deck'''
    def __init__(self):
        '''Generates 52 cards'''
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.cards.append(card)

    def deal(self, hand, num):
        '''Deals cards from deck to another hand'''
        while num > 0:
            cards_dealt = self.cards.pop()
            hand.cards.append(cards_dealt)
            num -= 1
