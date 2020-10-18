import tkinter as tk
import random
import parse


colors = ["blue","red","orange","green","purple"]
placements = []


class Text(tk.Label):
    """This class is used to generate the words in the word cloud. Also is used to create hover over text in second frame."""
    def __init__(self,mainFrame,secondFrame, word, count, charDic,hoverLabel):
        self.label = tk.Label(mainFrame, text=word)
        self.count = count
        self.word = word

        self.hoverLabel = hoverLabel
        self.charDic = charDic



        self.label.bind("<Enter>", self.on_enter)
        self.label.bind("<Leave>", self.on_leave)

    def hoverText(self):
        hoverString = "Word: "+self.word + "\nTotal : "+ str(self.count)+"\n"
        
        tupleList = []
        for char in self.charDic: 
            if(self.word in self.charDic[char]):
                tupleList.append( (char,self.charDic[char][self.word]) )
        sort_orders = sorted(tupleList, key=lambda x: x[1], reverse=True)
        for i in sort_orders:
            char = i[0]
            charCount = i[1]
            hoverString+="{0:20} : {1:2} \n".format(char,charCount)

          
        return hoverString

    def on_enter(self,event):
        hoverString = self.hoverText()
        self.hoverLabel.configure(text=hoverString)

    def on_leave(self, enter):
        self.hoverLabel.configure(text="")

def place_label(root, label, word,fontSize,dic={}):
    """This function is the algorithm to generate the word cloud word placements.
    
    Args:
        root: tk root
        label: tk label for word
        word: string of word
        fontSize: int for font size of word to be used
        dic: dictionary that will contain all the labels that will be made.
             we will use this dictionary to edit existing labels for when we want to create new word cloud based on character's words
    """
    redo = True
    tries = 0
    
    colorIndex=random.randint(0,len(colors))-1
    #algorithm to make sure word is not placed in same location as another word
    while redo:
        if(tries>500):
            newFont=10
            label.config(font=("Courier", newFont),fg=colors[colorIndex])
        elif(tries>1000):
            newFont=5
            label.config(font=("Courier", newFont),fg=colors[colorIndex])
        else:
            label.config(font=("Courier", fontSize),fg=colors[colorIndex])
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
    # test[word][1]=place
    
def createWordCloud(root,mainFrame,secondFrame, tuples, charDic, hoverLabel,tupleFontSizeList):
    """This function generates words and places the words in the frames
    
    Args:
        root: tk root
        mainFrame: tk frame
        secondFrame: tk frame
        tuples: list of tuples of word and count
        charDic: dictionary of character and word with count
        hoverLabel: tk label of hover text 
        newTupleSizes: list of tuple of wordcount and font size
    """


    # print(len(tuples))
    # test = {}
    #tuples is a list of tuples. example: [(word, count), (word2, count)]
    index = 0
    for tup in tuples:
        word = tup[0]
        count = tup[1]
        text = Text(mainFrame,secondFrame,word,count,charDic,hoverLabel)

        # label = tk.Label(mainFrame, text=word)

        # test[tup[0]]=[label,[]]
        size = tupleFontSizeList[index][1]

        place_label(root, text.label, word,size)
        index+=1

#to do: when character button is pressed generate new word cloud based on only that character's words
def createWordCloudChar(test,dic,tuples):
    for tup in tuples: 
        if(tup[0] in emmet):
            test[tup[0]][0].place(x=test[tup[0]][1][2],y=test[tup[0]][1][5])
            size = emmet[tup[0]]
            test[tup[0]][0].config(font=("Courier", size),fg="blue")
        else:
            test[tup[0]][0].place(x=test[tup[0]][1][2],y=test[tup[0]][1][5])
            # size = emmet[tup[0]]
            test[tup[0]][0].config(font=("Courier"),fg="gray")
            

def testCommand():
    # tkMessageBox.showinfo( "Hello Python", "Hello World")
    print("pressed button")


def parseFunction(fileName,amountOfCommon):
    #Our movie transcript string path of txt file using this transcript format only works so far https://www.imsdb.com/scripts/Kung-Fu-Panda.html/ 
    textFileName = fileName

    #create our own stopword list since nltk's stopword list may not remove all stopwords we need.
    #stopwords from https://www.ranks.nl/stopwords
    stopwords = parse.createNewStopwords('stopwords.txt')

    #parse the text and get the dialogue only text and also the character word counter dictionary
    spoken_text, charWordDic =  parse.parseText(textFileName)

    #remove stopwords from dictionary 
    charWordDic =  parse.removeStopwordsDic(charWordDic,stopwords)

    #Get amount most common words from dialogue text
    common =  parse.commonWords(spoken_text,amountOfCommon,stopwords)

    # #string that is formated to show only the words that each character said that is commonly said throughout the text 
    # formatedString =  parse.formatnSortByChar(charWordDic,spoken_text,common)

    return charWordDic, common




def createRangeList(countList):
    newSet=[]
    maxNum = max(countList)
    for num in countList:
        if(num in range(maxNum-7,maxNum)):
            continue
        else:
            if(num not in newSet):
                newSet.append(num)
            maxNum = num

    return newSet

def generateNewSizes(tupleList,sizes):
    countList = [i[1] for i in tupleList]
    rangeList = createRangeList(countList)
    newSizeList = []
    newTupleList = []
    for count in countList:
        added = False
        for index in range(0,len(rangeList)-1):
            if(count in range(rangeList[index+1],rangeList[index]+1)):
                added = True
                newSizeList.append(sizes[index])
                break
        if(not added):
            newSizeList.append(sizes[len(sizes)-1])

    for count in range(0,len(newSizeList)):
        newTupleList.append( (tupleList[count][1],newSizeList[count] ) )

    return newTupleList

def main():

  #run parse function
  fileName  = "KungFuPanda.txt"
  amountOfCommon = 100
  charWordDic , common = parseFunction(fileName,amountOfCommon)

  #Default Sizes
  sizes=[65,35,20,15,10]

  #generate wordCloud text sizes using default sizes. returns list tuple of (count,FontSize)
  tupleFontSizeList = generateNewSizes(common,sizes)


  #Generate UI
  root = tk.Tk()
  root.geometry("1124x768")


  mainFrame = tk.Frame(root, width=824, height=750)
  secondFrame = tk.Frame(root, width=192, height=750)

  mainFrame.config(bd=4, relief=tk.SOLID)
  secondFrame.config(bd=4, relief=tk.SOLID)


  #this will be the character buttons will probably create for loop and generate multiple buttons
  # button = tk.Button (secondFrame, text = "test",width = 192,command=testCommand)
  # button.pack(side="top", fill="both")

  #Hover Overable label
  hoverLabel = tk.Label(secondFrame, text="", width=192)
  hoverLabel.config(font=("Courier", 10))
  hoverLabel.pack(side="top", fill="both")

  #Create Main Word Cloud
  #using common as a list of tuples that contain word and count. 
  createWordCloud(root,mainFrame,secondFrame,common, charWordDic, hoverLabel, tupleFontSizeList)

  #left frame and right frame
  mainFrame.pack(side="left", fill="both")
  secondFrame.pack(side="right", fill="both")

  root.mainloop()

main()