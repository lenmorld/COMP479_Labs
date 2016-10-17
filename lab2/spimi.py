from collections import OrderedDict
import sys
import linecache
import pprint
import ast

import filestuff

# def add_to_dictionary(dictionary, term):
#     dictionary[term] = []
#     return dictionary[term]
#
# def add_to_postings_list(postings_list, docID):
#     if docID not in postings_list:
#         postings_list.insert(0,docID)
#
# def get_postings_list(dictionary, term):
#     return dictionary[term]


"""
SPIMI()

input: token_stream - list of tokens - (term, docID) pair
"""
def SPIMI(token_stream, block_size):
    print("block_size: " + str(block_size))
    spimi_files = []
    spimi_file_count = 0
    dictionary = {}
    # pprint.pprint(token_stream)
    token_count = len(token_stream)
    token_ctr = 0

    for token in token_stream:
        token_ctr += 1
        term = token["term"]
        docID = token["docID"]

        if term in dictionary:
            if docID not in dictionary[term]:
                dictionary[term].append(docID)
        else:
            dictionary[term] = [docID]

##        if term == 'akira':
##            print(dictionary[term])
##            x = raw_input("PAUSE")
##            print(dictionary)
        # print(str(sys.getsizeof(dictionary)))

        # if it becomes too big for the block size, or it is the last document (indicated by the last token)
        if (sys.getsizeof(dictionary) > block_size) or (token_ctr >= token_count) :
            print(str(sys.getsizeof(dictionary)))
##            x = raw_input("PAUSE")
##            pprint.pprint(dictionary)
            sorted_dictionary = sort_terms(dictionary)

            spimi_file_count += 1
            spimi_file = write_block_to_disk(sorted_dictionary, spimi_file_count)    # generate block file for tokens_list
            spimi_files.append(spimi_file.name)         # add filename to the file list,   append(spimi_file) would add file objects
            # print("------------ SPIMI-generated dictionary block ------------------")
            dictionary = {}        # clear dictionary and postings list
            # print("------------ wrote to block# " + str(spimi_file_count) + "------------------")

    return spimi_files



def sort_terms(dictionary):
    # sorted(a, key = lambda tup: tup[0], reverse=True)
    #temp = OrderedDict(sorted(dictionary.items(), key=lambda(k,v):(k,v)))
    #return temp.items()
    sorted_terms = sorted(dictionary)
    dictionary_sorted = OrderedDict()
    for item in sorted_terms:
    	dictionary_sorted[item] = dictionary[item]

    return dictionary_sorted
    #dictionary = dictionary_sorted
    #dictionary_sorted = {}

    #dictionarySorted = OrderedDict(sorted(dictionary.items(), key=lambda(k,v):(k,v)))

# def write1(dictionary, file_count):
#     with open('block' + str(file_count) + '.txt', "w") as out_file:
#         write_block_to_disk(dictionary, out_file)
#     return out_file

def write_block_to_disk(sorted_terms, file_count):
    out_file = './blocks/block' + str(file_count) + '.txt'
    with open(out_file, "w") as out_file:
    #pickle.dump(sorted_terms, out_file)
        for item in sorted_terms:
            out_file.write(str(item) + ":" + str(sorted_terms[item]) + "\n")
    return out_file

# with open("log.txt") as infile:
#     for line in infile:
#         do_something_with(line)



#TESTING
# block_path = './blocks'
# filenames = filestuff.get_files(block_path, '.txt')



def block_merge(block_filenames):

    block_count = len(block_filenames)
    index_file = './blocks/index.txt'

    block_ctr = 1
    blocks = {}
    line_ctrs ={}

    for f in block_filenames:
        blocks[block_ctr] = f
        line_ctrs[block_ctr] = 1
        block_ctr += 1

    print("Blocks:")
    print(blocks)
    sorted_lines = []
    index = []
    finished_blocks = []

    filestuff.delete_content(index_file)  # clear contents of file before writing in a loop

    while len(finished_blocks) < block_count :
        with open(index_file, 'a+') as index_f:
            lines=[]
            for x in range(1,block_count+1):    # go through all blocks
                if x in finished_blocks:        # if block is finished, skip this
                    continue
                line = {}
                term = linecache.getline(blocks[x], line_ctrs[x])    # get line(posting) where the block pointer currently is
                # print 'term: ', term
                if term == '':                  # EOF, flag this block as finished
                    finished_blocks.append(x)
                else:                           # get line (posting) from this block, and collect them into a list
                    line['term'] = term
                    line['blockID'] = x
                    lines.append(line)
            # pprint.pprint(sorted_lines)
            if (len(lines) > 0):                                # if list of lines collected has at least one item
                min_line = min(lines, key=lambda t:t['term'])   # get minimum based on term
                min_block_id = min_line['blockID']                  # get blockID

                #disect entry into term and postings
                t_split = min_line['term'].split(':')
                d_term = t_split[0]
                postings = ast.literal_eval(t_split[1])         # convert postings string to list e.g. '[7,9]\n' -> [7,9]


                for l in lines:
                    if l['blockID'] != min_block_id:
                        other_block_id = l['blockID']
                        t_split_other = l['term'].split(':')
                        d_term_other = t_split_other[0]
                        postings_other = ast.literal_eval(t_split_other[1])         # convert postings string to list e.g. '[7,9]\n' -> [7,9]

                        if d_term == d_term_other:   # similar term: min term and one of the others
                            # postings = postings + postings_other    # merge them -> this would keep duplicates
                            postings = postings + list(set(postings_other) - set(postings))          # this would be an effective set union
                            line_ctrs[other_block_id] += 1          # make this other posting point to next line
                            min_line['term'] = str(d_term) + ":" + str(postings) + "\n"

                postings = sorted(postings)
                final_posting = str(d_term) + ":" + str(postings) + "\n"
                index.append(final_posting)                     # add to final_index
                index_f.write(final_posting)

                sorted_lines.append(min_line)                   # TESTING
                line_ctrs[min_block_id] += 1                    # increment pointer to this block to next line (posting)

            # print 'min: ', min_line

    #pprint.pprint(sorted_lines)    #in-memory
    #pprint.pprint(index)           #FILE

    return index_file

# for f in filenames:
#     block = {}
#     block['id'] = block_ctr
#     block['file'] = f
#     block['line'] = 1
#     blocks.append(block)
#     block_ctr += 1
#
#
# pprint.pprint(blocks)
#
#
# ctr = 0
# block_ctr = 1
#
# while ctr < 15:
#
#     print(linecache.getline(blocks[block_ctr]['file']))
#     block_ctr +=1
#     ctr +=1

# blocks = [None] * (block_count)  # init. list of size N
# block_ctr = 0
# line_ctrs = [1] * block_count    # init. line_ctr for each block
# print(block_count)
# print(line_ctrs)
# for f in filenames:
#     blocks[block_ctr] = f
#     block_ctr += 1
#
# print(blocks)
#
# while True:
#     lines = []
#     for x in range(block_ctr):
#         lines[x] = linecache.getline(blocks[x], line_ctrs[x])
#         print(lines[x])
#     line_ctrs[x] += 1

#     print(linecache.getline(f, 2))
#
#
# while ctr < 20:
#     print(linecache.getline(f[block_ctr], 2))

    # get minimum line, in terms of lexicographic order
    # whichever file contains min should move pointer to next one
    # if no minimum, they are all the same,

# def intersect(blk1, vblk2):
#     while blk1 != {} and blk2 != {}:
#         term1 = getTerm(blk1)
#         term2 = getTerm(blk2)
#
#         if term1 == term2
#             pos = merge_posting
#             add (term1, pos)
#
#           term1 = nextTerm(blk1)
#           term2 = nextTerm(blk2)
#         else if term1 < term2
#             add (term1, pos)
#             term1 = nextTerm(blk1)
#         else
#             add (term2, pos)
#             term2 = nextTerm(blk2)
