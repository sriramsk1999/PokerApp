import random
import pprint

def gen_game(nplayers): # readies cards for players and table
    player = [[] for i in range(nplayers)]
    table = []
        
    for i in range(nplayers): #number of players
        while(len(player[i])!=3): #3 cards for each playerstr(num[random.randint(0,12)]) 
            card = str(num[random.randint(0,12)]) + ' of ' + suit[random.randint(0,3)]
            if(card in allcards):
                player[i].append(card)
                allcards.remove(card)
        while(len(table)!=5):
            card = str(num[random.randint(0,12)]) + ' of ' + suit[random.randint(0,3)]
            if(card in allcards):
                table.append(card)
                allcards.remove(card)
    return player,table

def winner(player,table):
    print("TODO")

global allcards
num = list(range(13))
suit = ['club','spade','diamond','heart']
allcards = [str(i) + " of " + j for i in num for j in suit]

nplayers=int(input())
player,table = gen_game(nplayers)    
pprint.pprint(player)
pprint.pprint(table)
winner(player,table)
       