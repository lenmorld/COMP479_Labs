import nltk
import json
from nltk.stem.porter import *
import sys

from normalize import *
from sgml_parser import *
from counter import *
from spimi_methods import *


####### Memory management ######## 
block_size = 100


file1 = "./docs/reut2-021.sgm"

count_body = count_body(file1)   # number of body tags in the file
docs = extract(open(file1), count_body)

doc_ctr = 1
in_index = {}

spimi_files = []
spimi_file_count = 0

# token_stream should be a list of (term, docID) pair
def SPIMI(token_stream):
    global spimi_file_count
    
    spimi_file_count += 1
    with open('block' + str(spimi_file_count) + '.bin', "wb") as out_file:
    
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


            #if (sys.getsizeof(dictionary)/1024/1024) >= block_size:
            #    break

        pprint.pprint(dictionary)
        # x = raw_input("PAUSE")

        ########## TODO ############
        #### nothing working beyond this point at SPIMI #####
            
        # at this point, we have an inverted index for a block : dictionary
        
        write_block_to_disk(dictionary, out_file)            
            
            # merge_blocks()
        #out_file.close()

    return out_file.name

#####################################################
#################### MAIN ###########################
#####################################################

#with open('block.bin', "wb") as out_file:

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
        tokens_list.append(token_obj)
        
    #print("TOKEN LIST---------------------------")
    pprint.pprint(tokens_list)

    if sys.getsizeof(tokens_list) >= block_size:
        spimi_file = SPIMI(tokens_list)
        spimi_files.append(spimi_file)
    print("------------ finished a doc------------------")
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

d_ctr = 0
for f in spimi_files:
    with open(f,'rb') as file1:   
        data1 = pickle.load(file1)
        print("doc: " + f + "_" )
        pprint.pprint(data1)
        d_ctr += 1
        





