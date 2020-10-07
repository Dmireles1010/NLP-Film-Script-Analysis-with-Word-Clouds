import codecs
import re
import nltk
nltk.download('stopwords')

# stopwords from https://www.ranks.nl/stopwords

#character with dic of words with amount of times said
#character : {word : 2 , wordtwo : 4}
charWordDic = {}

textFileName = 'KUNG FU PANDA Script.txt'

def stripExtra(name):
  startIndexPer=name.find('(')

  start = 0
  if(startIndexPer!=-1):
    start = startIndexPer

  if(start==0):
    return name
  else:
    return name[0:start-1]

def parseText(textFileName):
  # https://stackoverflow.com/a/49866802
  # using https://www.imsdb.com/scripts/Joker.html as script. Highlight/copy script and save to a text file
  with codecs.open(textFileName, 'r', 'utf8') as f:
    # read the file content
    f = f.read()
    # store all the clean text that's accumulated
    spoken_text = ''
    test = ''
    # once a character's name is found turn True in order to write the following lines of text into dialoug string
    currentlySpeaking = False
    # once a character's name is found turn True in order to write character's name in the beginning of dialoug string
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
      # https://stackoverflow.com/a/16084717
      nameStriped = [word for word in words if word.isalpha()]
      
      newSpacing = (len(line) - len(line.lstrip()))

      #this is used to distinuged between name and all caps text
      if (spacing ==  0):
          spacing = newSpacing

      if len(nameStriped) > 0 and len(nameStriped) <= 3 and len(nameStriped[0]) > 1 and (len(line) - len(line.lstrip()) < 45) and all([i.isupper() for i in nameStriped]) and spacing == newSpacing:
          currentSpeaker=line.strip()
          writtenName=False
          currentlySpeaking = True
          continue


      # if there's a good amount of whitespace to the left and currentlySpeaking boolean is true, this is a spoken line
      if (len(line) - len(line.lstrip()) > 4) and currentlySpeaking:
          #strip extra characters such as paranthesis 
          currentSpeaker=stripExtra(currentSpeaker)

          if '(' in line or ')' in line:
            continue
          #if writtenName boolean is false write the name of the speaker and then turn the boolean true
          if not writtenName:
            # spoken_text+="\n"+currentSpeaker + ": "
            writtenName=True

          #needed to know count of word by each character
          #Dictionary of Characters containning amount of words
          for word in words:
            if currentSpeaker not in charWordDic:
              charWordDic[currentSpeaker]={}
              word = re.sub(r"[^\w\s'-]", '', word) 
              charWordDic[currentSpeaker][word.lower()]=1
            else:
                word = re.sub(r"[^\w\s'-]", '', word) 
                if word.lower() not in charWordDic[currentSpeaker]:
                  charWordDic[currentSpeaker][word.lower()]=1
                else: 
                  charWordDic[currentSpeaker][word.lower()]+=1  


          #write the dialoug into after character's name or continue dialoug. 
          # spoken_text += line.lstrip()
          spoken_text+=re.sub(r"\(.*?\)", '', line.lstrip()) 


  return spoken_text, charWordDic

def commonWords(text):
  words = text.split()
  stopwords2 = nltk.corpus.stopwords.words()
  cleansed_words = [word.lower() for word in words if word.isalpha() and word.lower() not in stopwords and word.lower() not in stopwords2]
  vocabulary = set(cleansed_words)
  # print(len(vocabulary))

  fdist = nltk.FreqDist(cleansed_words)

  common=fdist.most_common(100)
  return common


def removeStopwordsDic(dic):
  stopwords2 = nltk.corpus.stopwords.words()
  characterDic={}
  for word in dic:
    if word.isalpha() and word.lower() not in stopwords and word.lower() not in stopwords2:
      characterDic[word]=dic[word]
  return characterDic


def formatnSortByChar(dic,spoken_text):
  common = commonWords(spoken_text)
  print(common)
  text = ''

  for character in dic:
    boolean = False
    characterDic = removeStopwordsDic(dic[character])
    sort_orders = sorted(characterDic.items(), key=lambda x: x[1], reverse=True)
    
    
    for i in sort_orders:
      if i[0] in [lis[0] for lis in common]:
        if not boolean:
          text +="\n\n"+ character
          boolean = True
        text+="\n"+ str(i[0])+ " "+ str(i[1])
  return text

#give each word said by each character a ratio based on amount said and how many characters said it.
def ratio(dic):
  return


spoken_text, charWordDic = parseText(textFileName)

#remove any character that is not a letter or ' from text 
spoken_text = re.sub(r"[^\w\s'-]", '', spoken_text) 
# print(spoken_text)

stopwords = []
with codecs.open('stopwords.txt', 'r') as f:
  line = f.readlines()
  for word in line:
    stopwords.append(word.strip())




# print(charWordDic)

# #Words said by each character in film 
print(formatnSortByChar(charWordDic,spoken_text))

# #Common Words said in all dialoug of film
# print(commonWords(spoken_text))
# print(spoken_text)

