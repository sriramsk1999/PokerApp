import socket
from poker_data import *
import random
import itertools
from copy import deepcopy
import time

_SUITS = [1 << (i + 12) for i in range(4)]
_RANKS = [(1 << (i + 16)) | (i << 8) for i in range(13)]
_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
_DECK = [_RANKS[rank] | _SUITS[suit] | _PRIMES[rank] for rank, suit in 
    itertools.product(range(13), range(4))]

SUITS = 'CDHS'
RANKS = '23456789TJQKA'
DECK = [''.join(s) for s in itertools.product(RANKS, SUITS)]
LOOKUP = dict(zip(DECK, _DECK))
deck=list(DECK)

port=12000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('',port))

#pre-game
def broadcast_players(players_game):
	#broadcasting player names and giving players cards
	player_cards=[]
	random.shuffle(deck)
	x=0
	for i in range(len(players_game)):
		reply='create_players,'
		player_cards.append(deck[x:x+2])
		card1, card2 = deck[x:x+2]
		reply=reply+player_cards[i][0]+','+player_cards[i][1]+','
		for j in range(len(players_game)):
			if(j!=i):
				reply=reply+players_game[j][0]+','       #list of player_names other than the player who it is being sent to
		server_socket.sendto(reply.encode(), (players_game[i][1],port))
		x+=2
	return player_cards,x  #for future cards		

def players_turn(players_round):
	for i in range(len(players_round)):
		msg = 'turn,'+players_round[i][0]
		server_socket.sendto(msg.encode(), (players_round[i][1],port))
		reply, clientAddress = server_socket.recvfrom(2048)
		reply=str(reply).split(',')
		if(reply[0]=='call'):
			for j in range(len(players)): #players because sent to everyone
				if(j!=i):
					msg = 'other_call,'+reply[1]+','reply[2]
					server_socket.sendto(msg.encode(), (players[j][1],port))
		else:	
			for j in range(len(players)):
				if(j!=i):
					msg = 'other_fold,'+reply[1]
					server_socket.sendto(msg.encode(), (players[j][1],port))
				else: #player who folded
					players_round.remove(players_round[j])
				if(len(players_round)==1):
					return players_round
	return players_round #modified by removing players who have folded

#adds cards to the table
def update_table(players,x,t,round_in_progress,table_cards):
	if(t==1): #theflop
		flop = deck[x:x+3]
		table_cards.extend(flop)
		flop = ','.join(flop)
		msg = 'theflop'+flop
		x+=3
	elif(t==2): #theturn
		turn = deck[x]
		table_cards.append(turn)
		msg = 'theturn'+turn
		x+=1
	elif(t==3): #theriver
		river = deck[x]
		table_cards.append(river)
		msg = 'theriver'+river	
		x+=1
	for i in range(len(players)):
		server_socket.sendto(msg.encode(), (players[i][1],port))	
	if(t>3): #round_over
		round_in_progress=False
	return x,round_in_progress,table_cards

def winner(player,table):
    scores=[]
    hands=deepcopy(player)
    table1=deepcopy(table)
    for i in range(len(hands)):
        hands[i].extend(table1)
        score=eval7(hands[i])
        scores.append(score)
    return scores.index(min(scores)) #winning hand

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

#players joining room
players = [] #list of tuples of the form - (playerName,clientAddress)
while(len(players!=5)):
	msg, clientAddress = server_socket.recvfrom(2048)
	msg=str(msg).split(',')
	if(msg[0]=='join'):
		players.append((msg[1],clientAddress))

'''
	players - initial list of people who connected
	players_game - players in the game, get game-specific information, reduced when people eliminated
	players_round - players in a round, reduced when people fold.

	Client messages
		join
		eliminated
		call
		fold
		not eliminated
'''
global players
game_in_progress=True
players_game = players.deepcopy() #players in the game
while(game_in_progress):

	player_cards, x = broadcast_players(players_game):
	table_cards = []
	round_in_progress=True
	t=1
	players_round = players_game.deepcopy()   #active players in a round

	while(round_in_progress):
		players_round = players_turn(players_round)
		if(len(players_round) == 1):
			break
		x,round_in_progress,table_cards=update_table(players,x,t,round_in_progress,table_cards)  #players instead of players_round because displayed to all players
		t+=1

	if(len(players_round) == 1):
		msg = 'round_over' + players_round[0] + player_cards
	else:
		i = winner(player_cards,table_cards)
		msg = 'round_over' + players_round[i] + player_cards
	for i in range(len(players)):
		server_socket.sendto(msg.encode(), (players[i][1],port))

	for i in range(len(players_game)):
		msg, clientAddress = server_socket.recvfrom(2048)
		msg = msg.split(',')
		if(msg[0]=='eliminated'):
			reply = 'player_elim' + msg[1]
			players_game.remove(players_game[i])
			for j in range(len(players)):
				server_socket.sendto(msg.encode(), (players[j][1],port))

	if(len(players_game) == 1):
		game_in_progress = False
		msg = 'game_over'+players_game[0][0]
		for i in range(len(players)):
			server_socket.sendto(msg.encode(), (players[i][1],port))

	time.sleep(3)