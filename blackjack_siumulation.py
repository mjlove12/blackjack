'''Monte Carlo Simulation for basic strategy in blackjack.
Playing card classes from greentea press ThinkPython book.'''

import math
import random

class Card(object):
    #Represents a standard playing card
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

    suit_names = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    rank_names = [None, 'Ace', '2', '3', '4', '5', '6', '7',
              '8', '9', '10', 'Jack', 'Queen', 'King']

    def __str__(self):
        return '%s of %s' % (Card.rank_names[self.rank],
                             Card.suit_names[self.suit])

    def __cmp__(self, other):
    # check the rank of the card
        if self.rank > other.rank:
            return 1

        elif self.rank < other.rank:
            return -1

        # ranks are the same... it's a tie
        else:
            return 0

class Hand(object):
    #Represents a collection of playing cards
    def __init__(self):
        self.cards = []

    def __str__(self):
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
    #Represents a type of hand that is a full deck and can be dealt

    def __init__(self):
        # the init method creates the attribute cards and generates 52
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.cards.append(card)

    def deal(self, hand, num):
        while num > 0:
            cards_dealt = self.cards.pop()
            hand.cards.append(cards_dealt)
            num -= 1



def update(choice, outcome, score, hits):
    '''Keeps track of the choice by the player and the outcome of the game.
    Returns a modified version of the "hits" dictionary when a hit leads
    to a succesful outcome.'''
    if choice == 1 and outcome == 1:
        hits[score] +=1
    elif choice == 0 and outcome == 0:
        hits[score] +=1
    else:
        pass

def play(player, dealer, scenarios, hits, deck):
    '''Simulates a turn in blackjack. '''
    score = (player.tally(), dealer.tally())
    scenarios[score] += 1 #Logging this instance
    if scenarios[score] == 0:
        #If this situation hasn't been encountered, randomly choose hit or stay
        x = random.randint(0,1)
        if x == 1:
            #HIT!
            choice = 1
            deck.deal(player, 1)
            if player.tally() <= 21:
                outcome = 1 #Good, didn't bust
            else:
                outcome = 0 #Bust
            update(choice, outcome, score, hits)
        else:
            #STAY!
            choice = 0
    else:
        #If encountered, choose based on past ratios of good to total outcomes
        x = random.uniform(0.0,1.0)
        #Percentage of times you should hit for the scenario
        r = hits[score]/scenarios[score]
        if x < r:
            #HIT!
            choice = 1
            deck.deal(player, 1)
            if player.tally() <= 21:
                outcome = 1
            else:
                outcome = 0
            update(choice, outcome, score, hits)
        else:
            #STAY
            choice = 0
    return choice

def play_game():
    #Simulates an entire hand of blackjack

    #Initiating objects
    dealer = Hand()
    player = Hand()
    deck = Deck()
    deck.shuffle()

    #Dealing the cards
    deck.deal(player, 2)
    deck.deal(dealer, 1)

    choice = 1

    #Stop if player has blackjack
    if player.tally() == 21:
        "Blackjack!"
    else:
        #Player turn
        while (choice == 1 and player.tally() <= 21):
            choice = play(player, dealer, scenarios, hits, deck)
        score = (player.tally(), dealer.tally())
        #Dealer turn - play until you get 17 or higher
        while dealer.tally() < 17:
            deck.deal(dealer,1)

    if player.tally() > 21:
        outcome = 0
    #print "Player bust, dealer wins!"

    elif dealer.tally() > 21:
        outcome = 1
    #print "Dealer bust, player wins!"

    elif dealer.tally() > player.tally():
        outcome = 0
    #print "Dealer Wins!"

    elif dealer.tally() == player.tally():
        outcome = 2
    else:
        outcome = 1
    #print "Player Wins!"

    if choice == 0:
        update(choice, outcome, score, hits)
    else:
        pass

#START OF SIMULATION
if __name__=="__main__":

    '''    Here is the game    '''

    print('Starting scipt...')

    scenarios = dict() #"matrix" of all possible scenarios the player can encounter
    hits = dict() #only records times that the player should have hit
    player_values = range(4,22) #player only has values 4 - 22
    dealer_values = range(2,12) #Dealer only has values 2 to 11. 12 to be safe.

    #Create the dictionaries that will be updated later
    for i in player_values:
        for j in dealer_values:
            scenarios[i, j] = 0.0
            hits[i, j] = 0.0

    print('Starting simulations...')

    i = 0
    #100,000 simulations of blackjack game
    while (i < 100000):
        play_game()
        i += 1
        #Print an update every 10,000 games
        if i in range(10000, 100000, 10000):
            print(str(int(i)) + ' Simulations done...')

    #END OF SIMULATION

    #Resulting hit percentages
    results = dict()
    for key in hits:
        if hits[key] > 0:
            results[key] = hits[key]/scenarios[key]

    #Creating logs specific to player_values only
    scenario_log = dict()
    hits_log = dict()

    #Writing results to two different files
    print('Writing Results...')
    for i in player_values:
        scenario_log[i] = 0.0
        hits_log[i] = 0.0
    f = open('blackjack_prob.csv', 'w')
    g = open('blackjack_stats.csv', 'w')

    for key in results:
        f.write(str(key[0])+'\t'+str(key[1])+'\t'+str(results[key])+'\n')
        scenario_log[key[0]] += scenarios[key]
        hits_log[key[0]] += hits[key]

    g.write('Player_Score'+'\t'+'Hit'+'\t'+'Total'+'\n')
    for key in scenario_log:
        g.write(str(key)+'\t'+str(hits_log[key])+'\t'+str(scenario_log[key])+'\n')

    print('Script Complete')
