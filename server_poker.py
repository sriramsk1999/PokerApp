import socket
from poker_data import *
import random
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
deck=list(DECK)

port=12001
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('',port))

#players joining room
players = [] #list of tuples of the form - (playerName,clientAddress)
while(len(players!=5)):
	msg, clientAddress = server_socket.recvfrom(2048)
	msg=str(msg).split(',')
	if(msg[0]=='join'):
		players.append((msg[1],clientAddress))

#broadcasting player names and giving players cards
random.shuffle(deck)
x=0
for i in range(len(players)):
	reply='create_players,'
	card1, card2 = deck[x:x+2]
	reply=reply+card1+','+card2+','
	for j in range(len(players)):
		if(j!=i):
			reply=reply+players[j][0]+','       #list of player_names other than the player who it is being sent to
	server_socket.sendto(reply.encode(), players[i][1])
	x+=2 


game_in_progress=True
while(game_in_progress):
	round_in_progress=True
	while(round_in_progress):
		#TODO	