##f = open('./animals','r')
### lines = f.readlines()
### print(lines)
##ctr = 0
##
##for line in f:
##    ctr += 1
##    print(line + " " + str(ctr) )
##

import nltk, pprint
# nltk.download()

##word = raw_input("Enter word to search:")
##print(word)

with open('./animals','r') as f:
    list1 = f.read().splitlines()

##print(list1)
ctr = 0

indexList = {}


# get tokens
for line in list1:
    ctr += 1
    tokens = nltk.word_tokenize(line)  # tokenize each line
    for token in tokens:
        if token not in indexList:
            list1 = []
            list1 += str(ctr)
            indexList[token] = list1
        else:
            indexList[token] =  indexList[token] + list(str(ctr))
        
pprint.pprint(indexList)
    

##for line in list1:
##    tokens = nltk.word_tokenize(line)  # tokenize each line
##    print(tokens)
    
##    ctr += 1
####    print(line + " " + str(ctr) )
##    print(tokens)
##
##    if word in line:
##        print(line + " " + str(ctr) )
##    else:
##        print(str(ctr))
        
