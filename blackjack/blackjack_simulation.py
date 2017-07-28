import math
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from cards import Card, Hand, Deck
from blackjack import Mtrx


'''START SIMULATION'''
mtrx = Mtrx()
#100,000 simulations of blackjack game
for i in range(1, 100000):
    deck = Deck()
    deck.shuffle()
    blackjack.play_round(mtrx, deck)

    #Print an update every 10,000 games
    if i in range(10000, 100000, 10000):
        print(str(int(i)) + ' Simulations done...')
'''END SIMULATION'''

#df = pd.DataFrame(mtrx.ratios.items())
df_list = []
for i in [mtrx.scenarios, mtrx.hits, mtrx.ratios]:
    df = pd.DataFrame.from_dict(i, orient='index')
    df = df.reset_index()
    df[['Player Score', 'Dealer Score']] = df['index'].apply(pd.Series)
    df = df.rename(columns={0: 'Value'})
    df = df.drop(['index'], axis = 1)
    df = df.groupby(['Player Score'], as_index=False).agg({'Value' : np.sum})
    df_list.append(df)
df_list[1] = df_list[1].rename(columns={'Value': 'Hits'})
df_list[0] = df_list[0].rename(columns={'Value': 'Scenarios'})
final = pd.merge(df_list[0], df_list[1], on='Player Score')
final['Hit Probability'] = final['Hits'] / final['Scenarios']
final = final[['Player Score','Hit Probability']]

plt.style.use('ggplot')
plt.figure()
final.plot(x='Player Score', kind='bar')
plt.show()
