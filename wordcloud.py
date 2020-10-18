import tkinter as tk
import random


# words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

words = ['fight', 'good', 'gonna', 'best', 'rocky', 'gotta', 'nothin', 'bad', 'creed', 'wanna', 'sure', 'great', 'shot', 'goin', 'kid', 'paulie', 'time', 'outta', 'talk', 'bum', 'feel', 'guy', 'left', 'rock', 'sister', 'gazzo', 'years', 'fightin', 'break', 'apollo', 'people', 'fifty', 'chance', 'gimme', 'broke', 'whatta', 'guys', 'business', 'three', 'apollo creed', 'boy', 'luck', 'house', 'fighter', 'real', 'hand', 'hear', 'listen', 'call', 'thing']

# words = ['fight', 'good', 'gonna', 'best', 'rocky', 'gotta', 'nothin', 'bad',]


#if a word has more than 3 words then place that one first.

placements = []
def place_label(canvas, label, word,randint):
    redo = True
    tries=0
    newLength=20

    while redo:
        if(tries>1000):
            newLength-=1
            label.config(font=("Courier",newLength))
        else:
            label.config(font=("Courier", randint))
        tries+=1
        root.update()
        width = label.winfo_reqwidth()
        height = label.winfo_reqheight()
        x = random.randint(0, 812-width)
        y = random.randint(0, 750-height)


        x2=x+width
        y2=y+height

        xmid = (x+x2)/2
        ymid = (y+y2)/2
        for placement in placements:
            #check if x is between a word that is already placed x,x2 coordinates, also check if the word is between our new word for safety measure.
            if(x > placement[0] and x < placement[1]) or (x2 > placement[0] and x2 < placement[1]) or (xmid > placement[0] and xmid < placement[1]) or (placement[2] > x and placement[2] < x2):
                if (y > placement[3] and y < placement[4]) or (y2 > placement[3] and y2 < placement[4]) or (ymid > placement[3] and ymid < placement[4]) or (placement[5] > y and placement[5] < y2):
                    redo = True
                    break
            else:
                redo = False
        if(len(placements)==0):
            redo = False

    label.place(x=x,y=y) 
    root.update()

    place = [x, label.winfo_width()+x, xmid, y, label.winfo_height()+y, ymid]

    placements.append(place)

    

root = tk.Tk()
root.geometry("1024x768")


mainFrame = tk.Frame(root, width=824, height=750)
secondFrame = tk.Frame(root, width=192, height=750)

mainFrame.config(bd=4, relief=tk.SOLID)
secondFrame.config(bd=4, relief=tk.SOLID)

# Sorts the contents of words in reverse alphabetical order
# words.sort(reverse=True)

# Sorts the contents of words by character length, short words first
sorted(words, key=len)

for word in words:
    label = tk.Label(mainFrame, text=word)
    place_label(mainFrame, label, word,random.randint(20, 50))


mainFrame.pack(side="left", fill="both")
secondFrame.pack(side="right", fill="both")


root.mainloop()
        
