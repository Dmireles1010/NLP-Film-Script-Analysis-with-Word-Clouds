import tkinter as tk
import random
import parse


colors = ["blue","red","orange","green","purple"]


#word:[label,place]
labelDic = {}
#label placement coordinates
placements = []
class Text(tk.Label):
    """This class is used to generate the words in the word cloud. Also is used to create hover over text in second frame."""
    def __init__(self,mainFrame,secondFrame, word, count, charDic,hoverLabel,individualChar=False,char=None):
        self.label = tk.Label(mainFrame, text=word)
        self.count = count
        self.word = word
        self.individualChar = individualChar
        self.char = char
        self.hoverLabel = hoverLabel
        self.charDic = charDic



        self.label.bind("<Enter>", self.on_enter)
        self.label.bind("<Leave>", self.on_leave)

    def hoverText(self):
        hoverString = "Word: "+self.word + "\nTotal : "+ str(self.count)+"\n"
        if(self.individualChar):
            hoverString=self.char+"\nWord: "+self.word + "\nTotal : "+ str(self.count)+"\n"
            return hoverString

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
        if(self.individualChar):
            self.hoverLabel.configure(text=self.char+"\nHOVER OVER A WORD TO VIEW DETAILS")
        else:
            self.hoverLabel.configure(text="HOVER OVER A WORD TO VIEW DETAILS")

def place_label(root, label, word,fontSize):
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
            redo=False
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
    labelDic[word]=[label,place]
    # test[word][1]=place
    
def createWordCloud(root,mainFrame,secondFrame, tuples, charDic, hoverLabel,tupleFontSizeList,individualChar=False,char=None):
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

    # test = {}
    #tuples is a list of tuples. example: [(word, count), (word2, count)]

    for word in labelDic:
        label = labelDic[word][0]
        label.destroy()
    labelDic.clear()
    placements.clear()



    index = 0

    for tup in tuples:
        word = tup[0]
        count = tup[1]
        text = Text(mainFrame,secondFrame,word,count,charDic,hoverLabel,individualChar,char)


        size = tupleFontSizeList[index][1]

        place_label(root, text.label, word,size)
        index+=1

def createWordCloudChar(char,root,mainFrame,secondFrame,charWordDic, hoverLabel,common,sizes):
    """This function generates words and places the words in the frames based on individual character
    
    Args:
        char : string of name
        root: tk root
        mainFrame: tk frame
        secondFrame: tk frame
        charWordDic: dictionary of character and word with count
        hoverLabel: tk label of hover text 
        common: list of tuple of word and wordcount  
        sizez: list of default sizes 
    """
    tupleList = []
    # charDic=parse.keepInCommon(charWordDic[char],common)
    for word in charWordDic[char]:
        tupleList.append (  (word,charWordDic[char][word])  )
    tupleFontSizeList = generateNewSizes(tupleList,sizes,True)


    # createWordCloud(root,mainFrame,secondFrame,common, newChar, hoverLabel, tupleFontSizeList)
    hoverLabel.configure(text=char+"\nHOVER OVER A WORD TO VIEW DETAILS")
    createWordCloud(root,mainFrame,secondFrame, tupleList, charWordDic, hoverLabel,tupleFontSizeList,True,char)

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

def createRangeList(countList,spreadAmount):
    newSet=[]
    maxNum = max(countList)
    for num in countList:
        if(num in range(maxNum-spreadAmount,maxNum)):
            continue
        else:
            if(num not in newSet):
                newSet.append(num)
            maxNum = num

    return newSet

def generateNewSizes(tupleList,sizes,individualChar=False):
    tupleList = sorted(tupleList, key=lambda x: x[1], reverse=True)

    countList = [i[1] for i in tupleList]
    if(individualChar):
        rangeList = createRangeList(countList,0)
    else:
        rangeList = createRangeList(countList,6)


    if(len(rangeList)>len(sizes)):
        rangeList=rangeList[0:len(sizes)-1]
    newSizeList = []
    newTupleList = []
    for count in countList:
        added = False
        for index in range(0,len(rangeList)-1):
            if(count in range(rangeList[index+1],rangeList[index]+1)):
                added = True
                newSizeList.append(sizes[index])
                break
        #hard coding this case. if all number counts are the same, set to default size of sizes[1]. 
        if(len(rangeList)==1):
            newSizeList.append(sizes[1])
            continue
        #last case for iteratin of loop
        if(not added):
            newSizeList.append(sizes[len(sizes)-1])

    for count in range(0,len(newSizeList)):
        newTupleList.append( (tupleList[count][1],newSizeList[count] ) )

    return newTupleList


def main():

  #run parse function
  fileName  = "FilmScripts/newBeemovie.txt"
  amountOfCommon = 100
  charWordDic , common = parseFunction(fileName,amountOfCommon)

  #Default Sizes
  sizes=[60,35,20,15,10]

  #generate wordCloud text sizes using default sizes. returns list tuple of (count,FontSize)
  tupleFontSizeList = generateNewSizes(common,sizes)


  #Generate UI
  root = tk.Tk()
  root.geometry("1124x768")


  mainFrame = tk.Frame(root, width=824, height=750)
  secondFrame = tk.Frame(root, width=192, height=750)




  mainFrame.config(bd=4, relief=tk.SOLID)
  secondFrame.config(bd=4, relief=tk.SOLID)

  newChar = {}
  for char in charWordDic:
    charDic=parse.keepInCommon(charWordDic[char],common)
    if(not charDic):
        continue
    else:
        newChar[char]=charDic
  #this will be the character buttons will probably create for loop and generate multiple buttons


  #Hover Overable label
  hoverLabel = tk.Label(secondFrame, text="HOVER OVER A WORD TO VIEW DETAILS", width=192)
  hoverLabel.config(font=("Courier", 10))


  #Create Main Word Cloud
  #using common as a list of tuples that contain word and count. 


  text = tk.Text(secondFrame, wrap="none")
  vsb = tk.Scrollbar(orient="vertical", command=text.yview)
  text.configure(yscrollcommand=vsb.set)


  text.insert("end", "Characters: \n")

  button = tk.Button (secondFrame, text = "ALL",command= lambda: createWordCloud(root,mainFrame,secondFrame,common, newChar, hoverLabel, tupleFontSizeList))
  text.window_create("end", window=button)
  text.insert("end", "\n")

  num = 0 
  for char in sorted(newChar):
    if(len(newChar[char])<3):
        continue
    name = char
    button = tk.Button (secondFrame, text = name,command= lambda name=char: createWordCloudChar(name,root,mainFrame,secondFrame,newChar,hoverLabel,common, sizes))
    text.window_create("end", window=button)
    text.insert("end", "\n")



  text.configure(state="disabled")


    
  createWordCloud(root,mainFrame,secondFrame,common, newChar, hoverLabel, tupleFontSizeList)

  #left frame and right frame
  mainFrame.pack(side="left", fill="both")
  secondFrame.pack(side="right", fill="both")
  hoverLabel.pack(side="top", fill="both")
  vsb.pack(side="right", fill="y")
  text.pack(fill="both", expand=True)

  root.mainloop()



  
if __name__ == "__main__":
    main()
