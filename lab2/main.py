import nltk
import json
from nltk.stem.porter import *


from normalize import *
from sgml_parser import *
from counter import *

file1 = "./reut2-021.sgm"

# words = ['cat','dog','sleep','the']

empty_words = ['',' ']
count_body = count_body(file1)   # number of body tags in the file
docs = extract(open(file1), count_body)

doc_ctr = 1

in_index = {}

for title,doc in docs.iteritems():
    ## tokenize SGM doc to a list

    print "Title:" ,title
    
    #terms = re.split('\s|(?<!\d)[,.](?!\d)', doc) # same as nltk.word_tokenize()
    terms = nltk.word_tokenize (doc)
    
    # print(terms)
    terms = [t for t in terms if (not t in empty_words)]

    ## normalize words
    normalized_words = normalize(terms)
    print("NORMALIZE---------------------------")
    pprint.pprint(normalized_words)

    ## stemming
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in normalized_words]

    ## build inverted index, docID would stand for each Reuters doc

    print("STEMMER---------------------------")
    pprint.pprint(tokens)

    # put in index
    print("INVERTED INDEX---------------------------")
    for token in tokens:
        if token not in in_index:
            list1 = []
            list1 += str(doc_ctr)
            in_index[token] = list1
        else:
            in_index[token] =  in_index[token] + list(str(doc_ctr))

    # next doc
    doc_ctr += 1


pprint.pprint(in_index)



