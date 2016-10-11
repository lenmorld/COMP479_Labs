import nltk
import json
from nltk.stem.porter import *
import sys

from normalize import *
from spimi_methods import *
import filestuff
import sgml_parser

####### Memory management ########
block_size = 1000
doc_path = './docs'

# file1 = "./docs/reut2-021.sgm"
reuter_files = filestuff.get_reuter_files(doc_path)

docs = {}


for reuter_file in reuter_files:
    new_docs = sgml_parser.extract(open(doc_path + '/' + reuter_file))
    docs = dict(docs.items() + new_docs.items())

def write1(dictionary, file_count):
    with open('block' + str(file_count) + '.bin', "wb") as out_file:
        write_block_to_disk(dictionary, out_file)
    return out_file

# token_stream should be a list of (term, docID) pair
def SPIMI(token_stream):
    spimi_files = []
    spimi_file_count = 0
    dictionary = {}

    for token in token_stream:
        term = token["term"]
        docID = token["docID"]

        if term not in dictionary:
            postings_list = add_to_dictionary(dictionary, term)
        else:
            postings_list = get_postings_list(dictionary, term)
        # if full(postings_list): double the postings_list
        add_to_postings_list(postings_list, docID)
        #if (sys.getsizeof(dictionary)/1024/1024) >= block_size:
        #    break
        if sys.getsizeof(dictionary) >= block_size:
            spimi_file_count += 1
            spimi_file = write1(dictionary, spimi_file_count)    # generate block file for tokens_list
            spimi_files.append(spimi_file)   # add file to the file list
            print("------------ SPIMI-generated dictionary block ------------------")
            pprint.pprint(dictionary)
            dictionary = {}         # clear dictionary
            print("------------ wrote to block# " + str(spimi_file_count) + "------------------")

            d_ctr = 1
            with open(spimi_file.name,'rb') as file1:
                data1 = pickle.load(file1)
                print("doc: " + spimi_file.name + "_" )
                pprint.pprint(data1)
                d_ctr += 1

            # x = raw_input("PAUSE")

        ########## TODO ############
        #### nothing working beyond this point at SPIMI #####
        # at this point, we have an inverted index for a block : dictionary
            # merge_blocks()
        #out_file.close()

    return spimi_files

#####################################################
#################### MAIN ###########################
#####################################################

#TODO: load all

#with open('block.bin', "wb") as out_file:

doc_ctr = 1
tokens_list = []

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

    for token in tokens:
        token_obj = {"term":token,"docID":doc_ctr}
        tokens_list.append(token_obj)

    print("finished doc" + str(doc_ctr))
    doc_ctr += 1    # next doc

    # x = raw_input("Next doc")

print("TOKEN LIST---------------------------")
pprint.pprint(tokens_list)

    # WRONG -- we have to collect all tokens, pass it to SPIMI and let SPIMI handle the blocks
    # if sys.getsizeof(tokens_list) >= block_size:
    #     spimi_file = SPIMI(tokens_list)  # generate block file for tokens_list
    #     spimi_files.append(spimi_file)   # add file to te file list
    # print("------------ finished a doc------------------")

spimi_files = SPIMI(tokens_list)

    # for block in spimi_files:
    #     print(block)


    #in_file = open("block.bin", "rb" )


##    for token in tokens:
##        if token not in in_index:
##            in_index[token] = doc_ctr
##        else:
##            in_index[token] =  in_index[token] + list(str(doc_ctr))



############ MERGING ##################
#-- finished reading all docs --
# now open files (and merge all blocks)
d_ctr = 0
for f in spimi_files:
    with open(f.name,'rb') as file1:
        data1 = pickle.load(file1)
        print("doc: " + f.name + "_" )
        pprint.pprint(data1)
        d_ctr += 1
