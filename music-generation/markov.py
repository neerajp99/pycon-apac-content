import pandas as pd 
import numpy as np
from collections import Counter 

def markov_chain_next_beat(beat):
    """Guess the next beat based on the frequency of succeeding beats
    """
    following_beats = [] 
    for value in language:
        if value.split(' ')[0] == beat:
            following_beats.append(value)
    value_count = dict(Counter(following_beats))
    for item in value_count.keys():
        value_count[item] = value_count[item] / len(following_beats)
    possibilities = []
    for val in value_count.keys():
        possibilities.append(val.split(' ')[1])
    return np.random.choice(possibilities, p = list(value_count.values()))

# Generate random beats from the markov chain 
def generate_text(beat, language, length):
    beats = list()
    for i in range(length):
        beats.append(markov_chain_next_beat(beat))
        beat = beats[-1]
    return beats
    
data = pd.read_csv('mj_beats.csv')

# Creating bigrams from the input data file 
mj_beats = data['beats'].values
probabilities = zip(*[mj_beats[i:] for i in range(2)])
language = [" ".join(p) for p in probabilities]
print(generate_text('A', language, 20))
