from tkinter import *
from PIL import ImageTk, Image
import string
import socket

class Player:
    def __init__(self,name):
        self.money=IntVar()
        self.money.set(100)
        self.name=name
        self.is_elim=False

    def create_label(self,window,*args):
        self.moneyLabel = Label(window, textvariable = self.money, bg="black", fg="red", font = "Arial 20 bold")
        if(args):
            self.moneyLabel.place(x=args[0],y=args[1])
        else:
            self.moneyLabel.pack(side = "bottom")
        self.playerLabel = Label(window, text = self.name, bg="black", fg="red", font = "Arial 20 bold")
        if(args):
            self.playerLabel.place(x=args[2],y=args[3])
        else:
            self.playerLabel.pack(side = "bottom")

    def create_image(self,window,card1,card2,x1,y1,x2,y2):
        self.card1_image = Image.open("images/"+card1+".jpg")
        self.card1_image = self.card1_image.resize((40, 50), Image.ANTIALIAS)
        self.card1_image = ImageTk.PhotoImage(self.card1_image)
        self.card1_image_label = Label(window, image = self.card1_image, width =30, height = 40) 
        self.card1_image_label.place(x = x1, y = y1)

        self.card2_image = Image.open("images/"+card2+".jpg")
        self.card2_image = self.card2_image.resize((40, 50), Image.ANTIALIAS)
        self.card2_image = ImageTk.PhotoImage(self.card2_image)
        self.card2_image_label = Label(window, image = self.card2_image, width =30, height = 40) 
        self.card2_image_label.place(x = x2, y = y2)     

def table(window):
    C = Canvas(window, bg="black", height=500, width=1050 ,bd = 0,borderwidth = 0, highlightthickness=0, relief='ridge')
    C.pack(side = "top")
    C.create_oval(40,40,1000,460,fill= "green",width = 10, outline = "brown")
    P = Label(window,textvariable = pot, bg="black", fg="red", font = "Arial 20 bold")
    P.pack(side = "right")

def table_cards(window,card1,card2,card3):

    #initial 3 cards to display. [Flop]
    global card_1_image,card_2_image,card_3_image

    card_1_image = Image.open("images/"+card1+".jpg")
    card_1_image = card_1_image.resize((70, 80), Image.ANTIALIAS)
    card_1_image = ImageTk.PhotoImage(card_1_image)
    card_1_image_label = Label(window, image = card_1_image, width =60, height = 70) 
    card_1_image_label.place(x = 450, y = 250)

    card_2_image = Image.open("images/"+card2+".jpg")
    card_2_image = card_2_image.resize((70, 80), Image.ANTIALIAS)
    card_2_image = ImageTk.PhotoImage(card_2_image)
    card_2_image_label = Label(window, image = card_2_image, width =60, height = 70) 
    card_2_image_label.place(x = 520, y = 250)

    card_3_image = Image.open("images/"+card3+".jpg")
    card_3_image = card_3_image.resize((70, 80), Image.ANTIALIAS)
    card_3_image = ImageTk.PhotoImage(card_3_image)
    card_3_image_label = Label(window, image = card_3_image, width =60, height = 70) 
    card_3_image_label.place(x = 590, y = 250)

    gameinfo.set("Flop")

def add_card(window,cardnum,card): #displaying turn and river
    global card_4_image,card_river_image
    if(cardnum==4):
        card_4_image = Image.open("images/"+card+".jpg")
        card_4_image = card_4_image.resize((70, 80), Image.ANTIALIAS)
        card_4_image = ImageTk.PhotoImage(card_4_image)
        card_4_image_label = Label(window, image = card_4_image, width =60, height = 70) 
        card_4_image_label.place(x = 660, y = 250) 
        gameinfo.set("Turn")

    else:    
        card_river_image = Image.open("images/"+card+".jpg")
        card_river_image = card_river_image.resize((70, 80), Image.ANTIALIAS)
        card_river_image = ImageTk.PhotoImage(card_river_image)
        card_river_image_label = Label(window, image = card_river_image, width =60, height = 70) 
        card_river_image_label.place(x = 730, y = 250)
        gameinfo.set("River")

def folded():
    msg = 'fold'+','+players[0].name
    client_socket.sendto(msg.encode(),addr)

    players[0].playerLabel.config(fg="yellow")
    gameinfo.set(players[0].name+" folds")
    call["state"] = "disabled"
    fold["state"] = "disabled"

def called(window): #on button click
    l = [str(i) for i in window.winfo_children()] #window.winfo_children() returns list of all widgets in the winodw
    if not(any(i.startswith('.!entry') for i in l)): #if entry widget doesn't exist
        e = Entry(window)
        e.pack(side = "bottom")	
        e.bind("<Return>", on_change)

def on_change(e):
    amount = int(e.widget.get())
    if(amount>0 and amount <= players[0].money.get()):  #if valid amount
        e.widget.delete(0, END)
        players[0].money.set(players[0].money.get()-amount)
        e.widget.destroy()
        gameinfo.set(players[0].name+" bets "+str(amount))
        pot.set(pot.get()+amount)

    msg = 'call'+','+players[0].name+','+str(amount)
    client_socket.sendto(msg.encode(),addr)
    	

def create_players(window,msg):      
    global call,fold
    call = Button(window, text = "Call", highlightbackground = "red", fg = "black", width = 8, activebackground = "black", activeforeground = "red", command = lambda: called(window))
    call["state"] = "disabled"   #disabled on startup until it is your turn
    call.pack(side = "bottom")
    fold = Button(window, text = "Fold", highlightbackground = "red", fg = "black", width = 8, activebackground = "black", activeforeground = "red", command = folded)
    fold["state"] = "disabled"
    fold.pack(side = "bottom")

    global players
    p1 = Player(msg[1])
    p1.create_label(window)

    p2 = Player(msg[2])
    p2.create_label(window,0,500,0,470)

    p3 = Player(msg[3])
    p3.create_label(window,0,120,0,90)     

    p4 = Player(msg[4])
    p4.create_label(window,1120,120,1120,90)

    p5 = Player(msg[5])
    p5.create_label(window,1120,500,1120,470)
    
    players=[p1,p2,p3,p4,p5]
    gameinfo.set("The game has started!")

def give_cards(window,card1,card2):
    players[0].create_image(window,card1,card2,640,550,600,550)
    if(not(players[1].is_elim)):
        players[1].create_image(window,"back","back",5,420,45,420)
    if(not(players[2].is_elim)):
        players[2].create_image(window,"back","back",5,40,45,40)
    if(not(players[3].is_elim)):
        players[3].create_image(window,"back","back",1120,40,1160,40)
    if(not(players[4].is_elim)):
        players[4].create_image(window,"back","back",1120,420,1160,420)   

def other_player_fold(player_who_folded_name):
    player_who_folded = get_player(player_who_folded_name)
    player_who_folded.playerLabel.config(fg="yellow")
    gameinfo.set(player_who_folded.name+ "has folded")

def other_player_call(player_who_called_name,amount):
    player_who_called = get_player(player_who_called_name)
    amount=int(amount)
    pot_change = pot.get()+amount
    pot.set(pot_change)
    player_who_called.money.set(player_who_called.money.get()-amount)
    gameinfo.set(player_who_called.name+" has called "+ str(amount))

def turn(player_name):
    player = get_player(player_name) 
    if player.name == players[0].name:
        call["state"] = "normal"
        fold["state"] = "normal"
    else:
        call["state"] = "disabled"
        fold["state"] = "disabled"

def game_over(window):
    window.destroy()

def change_card(player,new_card1,new_card2):
    player.card1_image = Image.open("images/"+new_card1+".jpg")
    player.card1_image = player.card1_image.resize((40, 50), Image.ANTIALIAS)
    player.card1_image = ImageTk.PhotoImage(player.card1_image)
    player.card1_image_label.configure(image=player.card1_image)

    player.card2_image = Image.open("images/"+new_card2+".jpg")
    player.card2_image = player.card2_image.resize((40, 50), Image.ANTIALIAS)
    player.card2_image = ImageTk.PhotoImage(player.card2_image)
    player.card2_image_label.configure(image=player.card2_image)

def player_elim(player_name):
    player = get_player(player_name)
    player.playerLabel.config(bg="white")
    player.is_elim = True
    gameinfo.set(player_name + " has been eliminated!")

def round_over(msg):
    gameinfo.set(msg[1]+" has won the round! Resetting table")
    player = get_player(msg[1])
    player.money.set(player.money.get() + pot.get())
    pot.set(0) 
    k = 0
    for i in range (2,len(msg)-1,2):
        if(players[k].is_elim):  #if player is eliminated they will not have cards to show
            continue
        change_card(players[k],msg[i],msg[i+1])
        k+=1
    if(players[0].money.get() == 0):
        msg = 'eliminated'+players[0].name
    else:
        msg = 'not_eliminated'
    client_socket.sendto(msg.encode(),addr)
    if(card_1_image):
        del card_1_image, card_2_image, card_3_image
        del card_1_image_label, card_2_image_label, card_3_image_label
    if(card_4_image):
        del card_4_image, card_4_image_label
    if(card_river_image): 
        del card_river_image, card_river_image_label
'''
Server Messages
    function               message from server                              comments

    create_players     "create_players,player_names_list"                 Creates players
    give_cards         "give_cards,card1,card2"                           Gives cards to players
    turn               "turn,player_name"                                 which player's turn it currently is
    table_cards        "theflop,card1,card2,card3"                        displays 3 cards on table
    add_card           "theturn,card4"                                    displays fourth card
    add_card           "theriver,card5"                                   displays fifth card
    other_player_call  "other_call,player_name,amount"                    the player who called and how much money 
    other_player_fold  "other_fold,player_name"                           the player who folded
    round_over         "round_over,winner_name,all cards"                 who won the round, display all other players' cards and then remove
    player_elim        "player_elim,player_name"                          a player who got eliminated
    game_over          "game_over,winner_name"                            who won the game
''' 
def server_listen(window): #listens for messages from server
    '''    
    msg="game_over,player5"

    if('card_1_image' not in globals()):
        table_cards(window,'KC','2H','AD' )
    if('players' not in globals()):
        create_players(window,['create_players','KC','QS','p1','p2','p3','p4','p5'])

    player_elim('p3')
    msg = ['round_over','p4','KC','QS','AD','AD','AD','AD','AD','AD','AD','AD']
    round_over(msg)
    '''
    try: #check if there is a message, if no message jump to except
        msg, serverIP = client_socket.recvfrom(2048)
        #msg='theflop,2H,2C,2D'   #Example Message
        msg=msg.decode().split(',')

        if(msg[0]=="game_over"):
            gameinfo.set(i.name+" has won the game!")
            window.after(5000,game_over,window) #end game after 5 seconds 
        elif(msg[0]=='create_players'):
            create_players(window,msg) #list other players' names
        elif(msg[0]=='give_cards'):
            give_cards(window,msg[1],msg[2])
        elif(msg[0]=='turn'):
            turn(msg[1])
        elif(msg[0]=='theflop'):
            table_cards(window,msg[1],msg[2],msg[3])
        elif(msg[0]=='theturn'):
            add_card(window,4,msg[1])
        elif(msg[0]=='theriver'):
            add_card(window,5,msg[1])
        elif(msg[0]=='other_call'):
            other_player_call(msg[1],msg[2])
        elif(msg[0]=='other_fold'):
            other_player_fold(msg[1])
        elif(msg[0]=='round_over'):
            round_over(msg) #passing the whole list because we don't know how many cards are being sent
        elif(msg[0]=='player_elim'):
            player_elim(msg[1])
        else:
            pass    
    except:
        pass
    finally:
        window.after(10,server_listen,window) #calls itself every 10 milliseconds listening for messages from server
    

def get_player(player_name):  #returns player object given player name
    for i in players:
        if i.name==player_name:
            return i

def join_game():
    popup = Tk()
    popup.title("Enter name")
    entry = Entry(popup)
    entry.pack(side='bottom') 
    entry.bind("<Return>", get_name)
    popup.mainloop()

def get_name(e):
    pname=e.widget.get()
    popup = e.widget.master
    popup.destroy()

    msg = 'join' + ',' + pname
    client_socket.sendto(msg.encode(),addr)


def main():
    global gameinfo,pot,cards,client_socket,addr
    ip = '127.0.0.1'  #change later
    port = 12000
    addr = (ip,port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setblocking(0) #non-blocking

    join_game()
    window = Tk()
    window.title("Poker")
    gameinfo = StringVar()
    gameinfo.set("Waiting....")
    pot = IntVar()
    pot.set(0)    
    window.configure(background = "black")
    center_name = Label(window, textvariable = gameinfo, bg="black", fg="white", font = "Helvetica 30 bold")
    center_name.pack(side="top")
    table(window)

    window.after(10,server_listen,window)
    window.mainloop()

main()