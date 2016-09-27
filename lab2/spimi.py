
free_memory = 100000000    #100 Million
block_size = 100000000      # 100 Million

postings_list = {}

# token_stream should be a (term, docID) pair
def SPIMI(token_stream):
    global block_ctr
    out_file = open("block.bin", "wb" ) as out_file:
    dictionary = {}
    
    block_ctr += 1
    out_file.write('haha')


    
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


def add_to_dictionary(dictionary, term):
    dictionary[term] = []
    return dictionary[term]

def add_to_postings_list(postings_list, docID):
    if docID not in postings_list:
        postings_list.insert(0,docID)

        

def get_postings_list(dictionary, term):
    return dictionary[term]

def sort_terms(dictionary):
    # sorted(a, key = lambda tup: tup[0], reverse=True)
    return sorted(dictionary)

def write_block_to_disk(sorted_terms, dictionary, out_file):
    pass
    
def merge_blocks():
    pass


SPIMI(None)
