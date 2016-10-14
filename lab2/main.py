import nltk
import json
import sys

from spimi_methods import *
import filestuff
import compress
import merge
import query

####### Memory management ########

# 8192 -> 2 blocks
memory_size = 10000
block_size = 8192


# ##### file management ##############
# # file1 = "./docs/reut2-021.sgm"
# reuter_files = filestuff.get_files(doc_path, '.sgm')
# docs = {}
# for reuter_file in reuter_files:
#     new_docs = sgml_parser.extract(open(reuter_file))
#     docs = dict(docs.items() + new_docs.items())

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
doc_path = './docs'
docs = filestuff.get_reuters(doc_path)

# do for each file in the collection
for title,doc in docs.iteritems():
    ## tokenize SGM doc to a list

    #-- BEFORE: simplest tokenizer, no filtering --
    terms = nltk.word_tokenize (doc)

    #-- AFTER: filters out punctuations
    # tokens = nltk.wordpunct_tokenize(doc)    # <-- SHIT THIS does case-folding too
    # text = nltk.Text(tokens)
    # terms = [w.lower() for w in text if w.isalnum()]

    # COMPRESSION 1
    # terms = compress.remove_numbers(terms)

    # --- no compression for now -----
    #terms = compress.normalize(terms)
    #terms = compress.p_stemmer(terms)

    for term in terms:
        token_obj = {"term":term,"docID":doc_ctr}
        tokens_list.append(token_obj)

    print("finished doc" + str(doc_ctr))
    doc_ctr += 1    # next doc

spimi_files = SPIMI(tokens_list)
print(spimi_files)

############ MERGING ##################
index_file = merge.block_merge(spimi_files)
print(index_file)


########### Query ####################

# put query loop here
# query1 = 'the'
# results = query.run_query(index_file, query1)

q1= query.QueryObject(index_file)

while True:
    print("Enter query separated by AND | OR:")
    query = raw_input(">")
    result = q1.run_query(query)
    print(query + '->')
    print(result)
# q1.run_query('a')
# q1.run_query('by')
# q1.run_query('but')
# q1.run_query('a AND by AND but')
# q1.run_query('a OR by OR but')
