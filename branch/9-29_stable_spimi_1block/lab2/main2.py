import nltk
import json
import sys
from nltk.stem.porter import *

from normalize import *
from sgml_parser import *
from counter import *
from spimi_methods import *

####### Files
file1 = "./docs/reut2-021.sgm"
docs = extract(open(file1), count_body)
count_body = count_body(file1)        # number of news articles in a file
doc_ctr = 1

####### Memory management 
block_size = 100000000

empty_words = ['',' ']
in_index = {}

# token_stream should be a (term, docID) pair
def SPIMI(token_stream):
    global block_ctr
    out_file = open("block.bin", "wb" )
    dictionary = {}
    
    block_ctr += 1

    while True:
        for token in token_stream:
            term, docid = token[0], token[1]
            if term not in dictionary:
                add_to_dictionary(dictionary, term)
            else:
                postings_list = get_postings_list(dictionary, term)
            # if full(postings_list): double the postings_list 
            add_to_postings_list(postings_list, docID)
        # at this point, we have an inverted index for a block
        sorted_terms = sort_terms(dictionary)
        write_block_to_disk(sorted_terms, dictionary, out_file)
        
        if (sys.getsizeof(dictionary)/1024/1024) >= block_size:
            break
            
    out_file.close()
    merge_blocks()


# do for each file in the collection

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
print(sys.getsizeof(in_index))

SPIMI(token_stream)

