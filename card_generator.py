import random
from poker_data import *
import itertools
from copy import deepcopy

_SUITS = [1 << (i + 12) for i in range(4)]
_RANKS = [(1 << (i + 16)) | (i << 8) for i in range(13)]
_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
_DECK = [_RANKS[rank] | _SUITS[suit] | _PRIMES[rank] for rank, suit in 
    itertools.product(range(13), range(4))]

SUITS = 'cdhs'
RANKS = '23456789TJQKA'
DECK = [''.join(s) for s in itertools.product(RANKS, SUITS)]
LOOKUP = dict(zip(DECK, _DECK))

def gen_game(nplayers): # readies cards for players and table
    player = [[] for i in range(nplayers)]
    table = []
    deck=list(DECK)
    random.shuffle(deck)
    table=deck[:5]
    for i in range(nplayers):
        player[i].append(deck[5+i])
    for i in range(nplayers):
        player[i].append(deck[5+nplayers+i])
    return player,table

def winner(player,table):
    scores=[]
    hands=deepcopy(player)
    table1=deepcopy(table)
    for i in range(len(hands)):
        hands[i].extend(table1)
        score=eval7(hands[i])
        scores.append(score)
    print("player",scores.index(min(scores))+1,"is the winner")
    return scores.index(max(scores))

def hash_function(x):
    x += 0xe91aaa35
    x ^= x >> 16
    x += x << 8
    x &= 0xffffffff
    x ^= x >> 4
    b = (x >> 8) & 0x1ff
    a = (x + (x << 2)) >> 19
    r = (a ^ HASH_ADJUST[b]) & 0x1fff
    return HASH_VALUES[r]

def eval5(hand):
    c1, c2, c3, c4, c5 = (LOOKUP[x] for x in hand)
    q = (c1 | c2 | c3 | c4 | c5) >> 16
    if (0xf000 & c1 & c2 & c3 & c4 & c5):
        return FLUSHES[q]
    s = UNIQUE_5[q]
    if s:
        return s
    p = (c1 & 0xff) * (c2 & 0xff) * (c3 & 0xff) * (c4 & 0xff) * (c5 & 0xff)
    return hash_function(p)

def eval7(hand):
    return min(eval5(x) for x in itertools.combinations(hand, 5))

nplayers=int(input())
player,table = gen_game(nplayers)    
print(player)
print(table)
winner(player,table)