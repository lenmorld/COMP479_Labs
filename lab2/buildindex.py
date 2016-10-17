import nltk
# import json
import pprint
import argparse

import filestuff
import spimi
import compress
# import merge
# import query

####### Memory management ########
memory_size = 1000000000
default_block_size = 2621440    # whole corpus 25MB/10 blocks = 2.5 MB

#################### MAIN ###########################
parser = argparse.ArgumentParser(description='build index', add_help=False)
parser.add_argument("block_size")
args = parser.parse_args()

if args.block_size:
    block_size = int(args.block_size)
else:
    block_size = default_block_size

print ("Using block size " + str(block_size))
# x = raw_input("Pause")

doc_ctr = 1
tokens_list = []
doc_path = './docs'
docs = filestuff.get_reuters(doc_path)

# do for each file in the collection
for title,doc in docs.iteritems():
    ## tokenize SGM doc to a list

    #-- BEFORE: simplest tokenizer, no filtering --
    terms = nltk.word_tokenize (doc)

    terms = compress.remove_weird_things(terms)           #1
    # terms = compress.remove_numbers(terms)              #2
    # terms = compress.case_folding(terms)                #3
    # terms = compress.remove_stop_words(terms)           #4

    for term in terms:
        token_obj = {"term":term,"docID":doc_ctr}
        tokens_list.append(token_obj)

    # print("finished doc" + str(doc_ctr))
    doc_ctr += 1    # next doc

# num_docs = doc_ctr

##pprint.pprint(tokens_list)
##x = raw_input("pause")
##tokens_list = compress.case_folding(tokens_list)        #3
##pprint.pprint(tokens_list)
##x = raw_input("pause")


####### STEMMING ##########
# TODO #

spimi_files = spimi.SPIMI(tokens_list, block_size)
print(spimi_files)

########## MERGING ##################
index_file = spimi.block_merge(spimi_files)
#print(index_file)


########### Query ####################
# put query loop here
# query1 = 'the'
# results = query.run_query(index_file, query1)

# q1= query.QueryObject(index_file)

# while True:
#     query = raw_input("Enter query separated by AND | OR:")
#     print(query + '->')
#     print(result)



# q1.run_query('a')
# q1.run_query('by')
# q1.run_query('but')
# q1.run_query('a AND by AND but')
# q1.run_query('a OR by OR but')
