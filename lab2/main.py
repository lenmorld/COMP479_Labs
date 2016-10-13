import nltk
import json
from nltk.stem.porter import *
import sys

from spimi_methods import *
import filestuff
import sgml_parser
import compress
import merge


####### Memory management ########
block_size = 8192
doc_path = './docs'

##### file management ##############
# file1 = "./docs/reut2-021.sgm"
reuter_files = filestuff.get_files(doc_path, '.sgm')
docs = {}
for reuter_file in reuter_files:
    new_docs = sgml_parser.extract(open(reuter_file))
    docs = dict(docs.items() + new_docs.items())

"""
SPIMI()

input: token_stream - list of tokens - (term, docID) pair
"""
def SPIMI(token_stream):
    spimi_files = []
    spimi_file_count = 0
    dictionary = {}
    # pprint.pprint(token_stream)
    for token in token_stream:
        term = token["term"]
        docID = token["docID"]

        if term in dictionary:
            if docID not in dictionary[term]:
                dictionary[term].append(docID)
        else:
            dictionary[term] = [docID]

        if sys.getsizeof(dictionary) >= block_size:
            sorted_dictionary = sort_terms(dictionary)

            spimi_file_count += 1
            spimi_file = write_block_to_disk(sorted_dictionary, spimi_file_count)    # generate block file for tokens_list
            spimi_files.append(spimi_file.name)         # add filename to the file list,   append(spimi_file) would add file objects
            # print("------------ SPIMI-generated dictionary block ------------------")
            dictionary = {}        # clear dictionary and postings list
            # print("------------ wrote to block# " + str(spimi_file_count) + "------------------")
    return spimi_files

#################### MAIN ###########################

doc_ctr = 1
tokens_list = []

# do for each file in the collection
for title,doc in docs.iteritems():
    ## tokenize SGM doc to a list
    terms = nltk.word_tokenize (doc)

    # --- no compression for now -----
    #terms = compress.normalize(terms)
    #terms = compress.p_stemmer(terms)

    tokens = terms

    for token in tokens:
        token_obj = {"term":token,"docID":doc_ctr}
        tokens_list.append(token_obj)

    print("finished doc" + str(doc_ctr))
    doc_ctr += 1    # next doc

spimi_files = SPIMI(tokens_list)

print(spimi_files)

############ MERGING ##################
index_file = merge.block_merge(spimi_files)
print(index_file)
