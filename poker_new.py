from tkinter import *
from PIL import ImageTk, Image
import string

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
	#send signal to server
    gameinfo.set("Player_1 folds")
    pass

def called(window): #on button click
    l = [str(i) for i in window.winfo_children()] #window.winfo_children() returns list of all widgets in the winodw
    if not(any(i.startswith('.!entry') for i in l)): #if entry widget doesn't exist
        e = Entry(window)
        e.pack(side = "bottom")	
        e.bind("<Return>", on_change)

def on_change(e):
    amount = int(e.widget.get())
    if(amount>0 and amount <= player_amt[0].get()):  #if valid amount
        e.widget.delete(0, END)
        player_amt[0].set(player_amt[0].get()-amount)
        e.widget.destroy()
        gameinfo.set("Player_1 bets "+str(amount))
        pot.set(pot.get()+amount)	

def players(window,card1,card2):
    global player1_card_1_image,player1_card_2_image 
    global player2_card_1_image,player2_card_2_image
    global player3_card_1_image,player3_card_2_image
    global player4_card_1_image,player4_card_2_image
    global player5_card_1_image,player5_card_2_image
    global player_amt
    player_amt = [IntVar(),IntVar(),IntVar(),IntVar(),IntVar()]
    for i in player_amt:
        i.set(100)          

    call = Button(window, text = "Call", highlightbackground = "red", fg = "black", width = 8, activebackground = "black", activeforeground = "red", command = lambda: called(window))
    call.pack(side = "bottom")
    fold = Button(window, text = "Fold", highlightbackground = "red", fg = "black", width = 8, activebackground = "black", activeforeground = "red", command = folded)
    fold.pack(side = "bottom")
    player1_money = Label(window, textvariable = player_amt[0], bg="black", fg="red", font = "Arial 20 bold")
    player1_money.pack(side = "bottom")
    player1_name = Label(window, text = "Client Player 1", bg="black", fg="red", font = "Arial 20 bold")
    player1_name.pack(side = "bottom") 


    player1_card_1_image = Image.open("images/"+card1+".jpg")
    player1_card_1_image = player1_card_1_image.resize((40, 50), Image.ANTIALIAS)
    player1_card_1_image = ImageTk.PhotoImage(player1_card_1_image)
    player1_card_1_image_label = Label(window, image = player1_card_1_image, width =30, height = 40) 
    player1_card_1_image_label.place(x = 640, y = 550)
    player1_card_2_image = Image.open("images/"+card2+".jpg")
    player1_card_2_image = player1_card_2_image.resize((40, 50), Image.ANTIALIAS)
    player1_card_2_image = ImageTk.PhotoImage(player1_card_2_image)
    player1_card_2_image_label = Label(window, image = player1_card_2_image, width =30, height = 40) 
    player1_card_2_image_label.place(x = 600, y = 550)
    

    player2_move = Label(window, text = "Move = ", bg="black", fg="red", font = "Arial 20 bold")
    player2_move.place(x = 0, y = 530)
    player2_money = Label(window, textvariable = player_amt[1], bg="black", fg="red", font = "Arial 20 bold")
    player2_money.place(x = 0, y = 500)
    player2_name = Label(window, text = "Client Player 2", bg="black", fg="red", font = "Arial 20 bold")
    player2_name.place(x = 0, y = 470)


    player2_card_1_image = Image.open("images/back.jpg")
    player2_card_1_image = player2_card_1_image.resize((40, 50), Image.ANTIALIAS)
    player2_card_1_image = ImageTk.PhotoImage(player2_card_1_image)
    player2_card_1_image_label = Label(window, image = player2_card_1_image, width =30, height = 40) 
    player2_card_1_image_label.place(x = 5, y = 420)
    player2_card_2_image = Image.open("images/back.jpg")
    player2_card_2_image = player2_card_2_image.resize((40, 50), Image.ANTIALIAS)
    player2_card_2_image = ImageTk.PhotoImage(player2_card_2_image)
    player2_card_2_image_label = Label(window, image = player2_card_2_image, width =30, height = 40) 
    player2_card_2_image_label.place(x = 45, y = 420)

    player5_move = Label(window, text = "Move = ", bg="black", fg="red", font = "Arial 20 bold")
    player5_move.place(x = 1120, y = 530)
    player5_money = Label(window, textvariable = player_amt[2], bg="black", fg="red", font = "Arial 20 bold")
    player5_money.place(x = 1120, y = 500)
    player5_name = Label(window, text = "Client Player 5", bg="black", fg="red", font = "Arial 20 bold")
    player5_name.place(x = 1120, y = 470)


    player5_card_1_image = Image.open("images/back.jpg")
    player5_card_1_image = player5_card_1_image.resize((40, 50), Image.ANTIALIAS)
    player5_card_1_image = ImageTk.PhotoImage(player5_card_1_image)
    player5_card_1_image_label = Label(window, image = player5_card_1_image, width =30, height = 40) 
    player5_card_1_image_label.place(x = 1120, y = 420)
    player5_card_2_image = Image.open("images/back.jpg")
    player5_card_2_image = player5_card_2_image.resize((40, 50), Image.ANTIALIAS)
    player5_card_2_image = ImageTk.PhotoImage(player5_card_2_image)
    player5_card_2_image_label = Label(window, image = player5_card_2_image, width =30, height = 40) 
    player5_card_2_image_label.place(x = 1160, y = 420)

    player3_move = Label(window, text = "Move = ", bg="black", fg="red", font = "Arial 20 bold")
    player3_move.place(x = 0, y = 150)
    player3_money = Label(window, textvariable = player_amt[3], bg="black", fg="red", font = "Arial 20 bold")
    player3_money.place(x = 0, y = 120)
    player3_name = Label(window, text = "Client Player 3", bg="black", fg="red", font = "Arial 20 bold")
    player3_name.place(x = 0, y = 90)


    player3_card_1_image = Image.open("images/back.jpg")
    player3_card_1_image = player3_card_1_image.resize((40, 50), Image.ANTIALIAS)
    player3_card_1_image = ImageTk.PhotoImage(player3_card_1_image)
    player3_card_1_image_label = Label(window, image = player3_card_1_image, width =30, height = 40) 
    player3_card_1_image_label.place(x = 5, y = 40)
    player3_card_2_image = Image.open("images/back.jpg")
    player3_card_2_image = player3_card_2_image.resize((40, 50), Image.ANTIALIAS)
    player3_card_2_image = ImageTk.PhotoImage(player3_card_2_image)
    player3_card_2_image_label = Label(window, image = player3_card_2_image, width =30, height = 40) 
    player3_card_2_image_label.place(x = 45, y = 40)

    player4_move = Label(window, text = "Move = ", bg="black", fg="red", font = "Arial 20 bold")
    player4_move.place(x = 1120, y = 150)
    player4_money = Label(window, textvariable = player_amt[4], bg="black", fg="red", font = "Arial 20 bold")
    player4_money.place(x = 1120, y = 120)
    player4_name = Label(window, text = "Client Player 4", bg="black", fg="red", font = "Arial 20 bold")
    player4_name.place(x = 1120, y = 90)
    
   
    player4_card_1_image = Image.open("images/back.jpg")
    player4_card_1_image = player4_card_1_image.resize((40, 50), Image.ANTIALIAS)
    player4_card_1_image = ImageTk.PhotoImage(player4_card_1_image)
    player4_card_1_image_label = Label(window, image = player4_card_1_image, width =30, height = 40) 
    player4_card_1_image_label.place(x = 1120, y = 40)
    player4_card_2_image = Image.open("images/back.jpg")
    player4_card_2_image = player4_card_2_image.resize((40, 50), Image.ANTIALIAS)
    player4_card_2_image = ImageTk.PhotoImage(player4_card_2_image)
    player4_card_2_image_label = Label(window, image = player4_card_2_image, width =30, height = 40) 
    player4_card_2_image_label.place(x = 1160, y = 40)

def server_listen(window): #listens for messages from server
    for i in range(len(flags)):
        flags[i]=True
    '''
    To-Do
    Messages from server
        flop - done
        turn - done
        river - done
        fold - when someone folds - {change colour of their name, change gameinfo}
        call - when someone else calls - {add money to pot, change gameinfo}
        round over - {change gameinfo to display winner,display all cards,remove all cards from table, update money of each player, reset pot, change player_name colours back to normal ...}
        game over - display winner
    '''        
    if(flags[0] and 'card_1_image' not in globals()):  #if flag is set and the image is not yet created
        table_cards(window,cards[('clubs','king')],cards[('hearts',2)],cards[('diamonds','ace')] )
    if(flags[1] and 'card_4_image' not in globals()):
        add_card(window,4,cards[('clubs',2)])
    if(flags[2] and 'card_river_image' not in globals()):
        add_card(window,5,cards[('clubs',5)])            
    window.after(10,server_listen,window)

def main():
    global gameinfo,pot,flags,cards
    flags=[False,False,False] #flags for flop, turn, river
    num = list(range(1,11))
    num[0] = 'ace';
    num.extend(['jack','queen','king'])
    suit = ['clubs','spades','diamonds','hearts']
    cards = {(i,j):str(j)+" of "+i for i in suit for j in num}

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
    players(window, cards[('clubs',2)],cards[('hearts','queen')])

    window.after(10,server_listen,window)
    window.mainloop()

main()