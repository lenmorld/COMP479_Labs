from collections import OrderedDict

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


def merge_blocks():
    pass
