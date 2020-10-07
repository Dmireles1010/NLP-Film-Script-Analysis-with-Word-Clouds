import codecs
import re
import nltk


def stripExtra(name):
  """This function removes paranthesis from a string
  *Can later be implemented for other uses like removing other characters from string
    
  Args:
      name (string): character's name

  Returns:
      string: character's name without paranthesis
  """
  startIndexPer=name.find('(')

  start = 0
  if(startIndexPer!=-1):
    start = startIndexPer

  if(start==0):
    return name
  else:
    return name[0:start-1]

def parseText(textFileName):
  """This function parses through a txt file that is formated as a transcript from the website https://www.imsdb.com/ 

  Args:
      textFileName (string): name/path of txt file of film transcript.

  Returns:
      (string,dictionary): a string of the dialogue text and
                           a dictionary of each characters said words in dialogue with word counter.
                           dictionary is formated as {character : {word : 2 , anotherword : 4} }
  """

  # using https://www.imsdb.com/ as script. Highlight/copy script and save to a text file
  charWordDic = {}
  with codecs.open(textFileName, 'r', 'utf8') as f:
    # read the file content
    f = f.read()
    # store all the clean text that's accumulated
    spoken_text = ''
    test = ''
    # once a character's name is found turn True in order to write the following lines of text into dialogue string
    currentlySpeaking = False
    # once a character's name is found turn True in order to write character's name in the beginning of dialogue string
    writtenName=False

    # string of current character that is speaking 
    currentSpeaker = ''

    spacing = 0
    # split the file into a list of strings, with each line a member in the list
    for line in f.split('\n'):
      # split the line into a list of words in the line
      words = line.split()
      # if there are no words, reset speaking and name booleans
      if not words:
          currentlySpeaking = False
          writtenName=False
          spacing = 0
          continue

      # if this line is a person identifier, save characters name into currentSpeaker string and adjust booleans 
      #Strip the name of non alphebetic characters
      nameStriped = [word for word in words if word.isalpha()]
      
      #used to determine if the following line is continuing the dialogue
      newSpacing = (len(line) - len(line.lstrip()))
      if (spacing ==  0):
          spacing = newSpacing

      #Keep track of person identifer and if its a new one or not
      #Name must be less than 3 words, length of name must not be less than 1, len of whitespace should be very long, name should be all uppercase, spacing and newSpacing should be the same since it is the start of the character's dialogue
      if len(nameStriped) > 0 and len(nameStriped) <= 3 and len(nameStriped[0]) > 1 and (len(line) - len(line.lstrip()) < 45) and all([i.isupper() for i in nameStriped]) and spacing == newSpacing:
          currentSpeaker=line.strip()
          writtenName=False
          currentlySpeaking = True
          continue


      # if there's a good amount of whitespace to the left and currentlySpeaking boolean is true, this is a spoken line
      if (len(line) - len(line.lstrip()) > 4) and currentlySpeaking:
          #strip extra characters such as paranthesis in character's name
          currentSpeaker=stripExtra(currentSpeaker)
          if '(' in line or ')' in line:
            #strip paranthesis from text since it's not dialogue 
            continue
          #if writtenName boolean is false write the name of the speaker and then turn the boolean true
          if not writtenName:
            # spoken_text+="\n"+currentSpeaker + ": "
            writtenName=True

          #Needed to know count of word by each character
          #Dictionary of Characters containning amount of words
          for word in words:
            if currentSpeaker not in charWordDic:
              charWordDic[currentSpeaker]={}
              #striping useless characters from word such as -- , . ? !
              word = re.sub(r"[^\w\s'-]", '', word) 
              charWordDic[currentSpeaker][word.lower()]=1
            else:
                word = re.sub(r"[^\w\s'-]", '', word) 
                if word.lower() not in charWordDic[currentSpeaker]:
                  charWordDic[currentSpeaker][word.lower()]=1
                else: 
                  #increment word count by one
                  charWordDic[currentSpeaker][word.lower()]+=1  


          # # write the dialogue into after character's name or continue dialogue. 
          # spoken_text += line.lstrip()

          #strip all words that are in paranthesis since it is not dialogue
          spoken_text+=re.sub(r"\(.*?\)", '', line.lstrip()) 

  #return the only the dialogue text and a dictionary of each characters said words in dialogue with word counter. Example: {character : {word : 2 , anotherword : 4} }
  return spoken_text, charWordDic

def commonWords(text,amount,stopwords):
  """This function finds the common words of a dialogue only script excluding character's names.
   
  Args:
      text (string): a corpus of only dialogue 

      amount (int): number of common words you'd like to be returned.

      stopwords (list): of your own stopwords

  Returns:
      list: a list of tuples that include the word and amount of times frequently said.
            list is formated as such: [(word,2),(anotherword,4),(newword,3)]
  """

  #splits the entire text into a list of words
  words = text.split()

  #second list of stopwords
  stopwords2 = nltk.corpus.stopwords.words()

  #removes all stopwords from the list of words
  cleansed_words = [word.lower() for word in words if word.isalpha() and word.lower() not in stopwords and word.lower() not in stopwords2]

  #using the nltk package, easily find most common words shown from the list of words
  fdist = nltk.FreqDist(cleansed_words)
  common=fdist.most_common(amount)

  #returns a list of tuples that include the word and amount of times frequently said
  return common

def removeStopwordsDic(dic,stopwords):
  """This function removes stopwords from the dictionary used in parseText(textFileName) function
   
  Args:
      dic (dictionary): a dictionary of each characters said words in dialogue with word counter.
                        dictionary is formated as such {character : {word : 2 , anotherword : 4} }

  Returns:
      dictionary: a dictionary of each characters said words in dialogue with word counter with no stopwords
                  dictionary is formated as such {character : {word : 2 , anotherword : 4} }
  """
  stopwords2 = nltk.corpus.stopwords.words()
  
  #create temp dictionary that will contain no stopwords
  characterDic={}
  
  for word in dic:
    #only include words not in stopword lists
    if word.isalpha() and word.lower() not in stopwords and word.lower() not in stopwords2:
      characterDic[word]=dic[word]

  #return a dictionary of each characters said words in dialogue with word counter with no stopwords. 
  #formated as such {character : {word : 2 , anotherword : 4} }
  return characterDic

def formatnSortByChar(dic,text,stopwords,common):
  """This function returns a formated string of the words each character has said in common with the text
   
  Args:
      dic (dictionary): a dictionary of each characters said words in dialogue with word counter.
                        dictionary is formated as such {character : {word : 2 , anotherword : 4} }

      text (string): a corpus of only dialogue 

      stopwords (list): of your own stopwords

      common (list): a list of tuples that include the word and amount of times frequently said.
                     list is formated as such: [(word,2),(anotherword,4),(newword,3)]

  Returns:
      text (string): a string that is formated to show only the words that each character said that is commonly said throughout the text 
                     Example: 
                            Character1
                            word 4
                            newword 3

                            Character2 
                            word 2

  """
  #remove any character that is not a letter or ' from text 
  text = re.sub(r"[^\w\s'-]", '', text) 

  text = ''

  for character in dic:
    boolean = False
    characterDic = removeStopwordsDic(dic[character],stopwords)
    sort_orders = sorted(characterDic.items(), key=lambda x: x[1], reverse=True)
    
    for i in sort_orders:
      #only show the words that are in common throughout the text
      if i[0] in [lis[0] for lis in common]:
        if not boolean:
          text +="\n\n"+ character
          boolean = True
        text+="\n"+ str(i[0])+ " "+ str(i[1])
  return text

#give each word said by each character a ratio based on amount said and how many characters said it.
def ComputeWeightedRatio(dic):
  """This function should create a weighted ratio based on amount of times the word was said by character, said throughout the film, and how many characters said that word
  
  Args:
      dic (dictionary): a dictionary of each characters said words in dialogue with word counter.
                        dictionary is formated as such {character : {word : 2 , anotherword : 4} }

  Returns:
      to be determined. probably best to return the same dictionary that will also include the ratio with the word count
  """
  return

def createNewStopwords(textFileName):
  """This function creates our own stopword list that we can use to remove from the dialogue text.
   
  Args:
      textFileName (string): name/path of txt file of stopwords where each word is in a new line.

  Returns:
      list: of stopword strings
  """
  stopwords = []
  with codecs.open(textFileName, 'r') as f:
    line = f.readlines()
    for word in line:
      stopwords.append(word.strip())
  return stopwords

def main():
  #download nltk stopwords list
  nltk.download('stopwords')
  
  #Our movie transcript string path of txt file 
  textFileName = 'KUNG FU PANDA Script.txt'

  #create our own stopword list since nltk's stopword list may not remove all stopwords we need.
  #stopwords from https://www.ranks.nl/stopwords
  stopwords = createNewStopwords('stopwords.txt')

  #parse the text and get the dialogue only text and also the character word counter dictionary
  spoken_text, charWordDic = parseText(textFileName)

  #Get 100 most common words from dialogue text
  common = commonWords(spoken_text,100,stopwords)

  #string that is formated to show only the words that each character said that is commonly said throughout the text 
  formatedString = formatnSortByChar(charWordDic,spoken_text,stopwords,common)

  #Common Words said in all dialogue of film
  print(common)

  #formated string of each character's said words that are commonly said through the dialogue
  print(formatedString)

main()


