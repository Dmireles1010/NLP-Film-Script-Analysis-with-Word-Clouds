  

import codecs
import re

def reduceLine(dialogue):
  keepReducing = True
  spokenTxt = ""
  while(keepReducing):
    
    space=dialogue.find(" ",34)
    newDialogue = dialogue[:space]

    spokenTxt+="\n              " + newDialogue.strip()
    dialogue=dialogue[space:]

    if(len(dialogue)>34):
      keepReducing = True
    else:
      keepReducing = False
  return spokenTxt
spokenTxt = '                            BEE MOVIE\n'
with codecs.open("originalBeeMovie.txt", 'r', 'utf-8') as f:
  # read the file content
  f = f.read()
  
  # split the file into a list of strings, with each line a member in the list
  for line in f.split('\n'):
    # split the line into a list of words in the line
    name = ''
    dialogue =''
    index = line.find(":")
    nameFound = False
    if(line.strip()==""):
      continue
    if(index!=-1):
      nameFound = True
      name = line[0:index]
      dialogue = line[index+1:]
      # print(name)
      # print(dialogue)
    else:
      dialogue=line.strip()

    if(nameFound): 
      spokenTxt+="\n\n                        "+name.upper()

    if(len(dialogue)>34):
      spokenTxt+=reduceLine(dialogue)

    else:
      spokenTxt+="\n              " + dialogue.strip()

  print(spokenTxt)


with codecs.open("NewBeeMovie.txt", 'w', 'utf-8') as f:
  f.write(spokenTxt)

