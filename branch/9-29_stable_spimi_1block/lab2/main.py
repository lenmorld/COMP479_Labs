import nltk
import json
from nltk.stem.porter import *
import sys

from normalize import *
from sgml_parser import *
from counter import *
from spimi_methods import *


####### Memory management ######## 
block_size = 10000000


file1 = "./docs/reut2-021.sgm"

count_body = count_body(file1)   # number of body tags in the file
docs = extract(open(file1), count_body)

doc_ctr = 1
in_index = {}


# token_stream should be a list of (term, docID) pair
def SPIMI(token_stream, out_file):
    
    dictionary = {}
    
    for token in token_stream:
        term = token["token"]
        docID = token["docID"]

        if term not in dictionary:
            postings_list = add_to_dictionary(dictionary, term)
        else:
            postings_list = get_postings_list(dictionary, term)
            
        # if full(postings_list): double the postings_list 
        add_to_postings_list(postings_list, docID)

        if (sys.getsizeof(dictionary)/1024/1024) >= block_size:
            break
    # TEST #
    pprint.pprint(dictionary)
    # x = raw_input("PAUSE")

    ########## TODO ############
    #### nothing working beyond this point at SPIMI #####
        
    # at this point, we have an inverted index for a block
    
    #pprint.pprint(dictionary)
    
    #x = raw_input("PAUSE")
    #sorted_terms = sort_terms(dictionary)
    #print("----sorted-------")
    #pprint.pprint(sorted_terms)
    #x = raw_input("PAUSE")

    write_block_to_disk(dictionary, out_file)            
        
        # merge_blocks()
    #out_file.close()

#####################################################
#################### MAIN ###########################
#####################################################

with open('block.bin', "wb") as out_file:

    # do for each file in the collection
    for title,doc in docs.iteritems():
        ## tokenize SGM doc to a list
        terms = nltk.word_tokenize (doc)
        ## normalize words
        normalized_words = normalize(terms)
        #print("NORMALIZE---------------------------")
        #pprint.pprint(normalized_words)

        ## stemming
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(word) for word in normalized_words]
        #print("STEMMER---------------------------")
        #pprint.pprint(tokens)
        
        ## build inverted index, docID would stand for each Reuters doc
        # put in index
        # print("INVERTED INDEX---------------------------")

        tokens_list = []
        
        for token in tokens:
            token_obj = {"token":token,"docID":doc_ctr}
            print(str(sys.getsizeof(tokens_list)))
            print(token)
            tokens_list.append(token_obj)
            
        #print("TOKEN LIST---------------------------")
        pprint.pprint(tokens_list)
        
        #x = raw_input("PAUSE")
        
        SPIMI (tokens_list, out_file)
        print("------------ finished a doc------------------")
        #x = raw_input("PAUSE")

        #in_file = open("block.bin", "rb" )
        
        
    ##    for token in tokens:
    ##        if token not in in_index:
    ##            in_index[token] = doc_ctr
    ##        else:
    ##            in_index[token] =  in_index[token] + list(str(doc_ctr))

        # next doc
        doc_ctr += 1



#-- finished reading all docs --
# now open files (and merge all blocks)

with open('block.bin','rb') as file1:
    d_ctr = 0
    while d_ctr < doc_ctr-1:
        data1 = pickle.load(file1)
        print("doc#: " + str(d_ctr+1))
        pprint.pprint(data1)
        d_ctr += 1
        





