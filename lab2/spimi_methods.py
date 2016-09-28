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
