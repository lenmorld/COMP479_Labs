from collections import OrderedDict
import ast
import argparse

class QueryObject:

    def __init__(self, index_file):
        self.index  = read_index_into_memory(index_file)

    @staticmethod
    def query_list(index, term_list, op):
        if len(term_list) >1:
            # get postings of first term

            try:
                temp_postings = index[term_list[0]]       # initialize with first term's docs
            except KeyError:
                temp_postings = list()

            and_postings = temp_postings                 
            and_postings_multiple = [temp_postings, ]     # accumulate intersection of documents per level ,e.g 1 doc, 2 docs 'and-ed', 3 docs 'and-ed', ...
            or_postings = temp_postings                  
            or_postings_multiple = [temp_postings, ]      # accumulate union of documents per level ,e.g 1 doc, 2 docs 'and-ed', 3 docs 'and-ed', ...

            #### doing OR with priority on the Intersections ###
            # to process OR, we need to order documents by how many keywords they contain
            # e.g. for a 3 word query, the first in the list should be the ones that contain all 3 keywords (i.e. the intersection of all 3)
            #       then the intersection of just 2 docs, and lastly the other docs that has either of the 3 but no intersection
            # to do that, we have to know the intersection and union at each level, in which level means incresing number of documents we are intersecting

            for t in term_list:
                try:
                    temp_term = index[t]
                except KeyError:
                    temp_term = list()

                and_postings = list(set(and_postings) & set(temp_term))
                and_postings_multiple.insert(0, and_postings)           # add the intersection of this much documents to the head of the list
                                                                        # at the end of the loop, we will have the intersection of all (or most) docs at the start of the list
                
                or_postings = list(set(or_postings) | set(temp_term))
                or_postings_multiple.insert(0, or_postings)
            if op == 'AND':
                return and_postings
            elif op == 'OR':
                # we want to put first the ones that have their intersection
                list_collector = []
                for and_postings_m in and_postings_multiple:        # go through all intersections, starting with the most 'encompassing' one
                    for item in and_postings_m:                     # for each intersection, get the list items
                        if item not in list_collector:              # instead of simply appending which will cause duplicates (and forced ordering for sets)
                            list_collector.append(item)             # we carefully append to the end of the final list, if item is not there yet

                for or_postings_m in or_postings_multiple:         # go through all unions, starting with the most 'encompassing' one
                    for item in or_postings_m:                     # for each union, get the list items
                        if item not in list_collector:              # instead of simply appending which will cause duplicates (and forced ordering for sets)
                            list_collector.append(item)             # we carefully append to the end of the final list, if item is not there yet

                return list_collector

        else:
            return index[term_list]




    def run_query(self, query):
        index = self.index
        q_split = query.split()

        if len(q_split) == 1:   # single word query
            try:
                result = index[query]
            except KeyError:
                result = "Term not found"
        else:                   # multiple query, separated by AND | OR
            if 'AND' in query:
                # multiple words query - cat AND dog
                try:
                    q_terms = query.split(' AND ')
                    result = QueryObject.query_list(index, q_terms, 'AND')
                except KeyError:
                    result = "one or all of the terms not found"
            elif 'OR' in query:
                # multiple words query - cat OR dog
                q_terms = query.split(' OR ')
                result = QueryObject.query_list(index, q_terms, 'OR')
            else:
                error_message = '''
                Unrecognized query:
                    usage: [term1]
                           [term1 AND term2 AND ...]
                           [term1 OR term2 OR ...]
                           [term1 OR term2 OR ...]
                '''
                return error_message

        # print(query + '->')
        # print(result)
        return result

def read_index_into_memory(index_file):
    index = OrderedDict()
    index_f = open(index_file)
    for line in index_f:
        t_split = line.split(':')
        term = t_split[0]
        postings = ast.literal_eval(t_split[1])         # convert postings string to list e.g. '[7,9]\n' -> [7,9]
        index.update({term:postings})
    print("Term count: " + str(len(index)))
    return index

############# MAIN ######################
parser = argparse.ArgumentParser(description='query', add_help=False)
parser.add_argument("query")
args = parser.parse_args()

# init index to use for querying
q1= QueryObject('./blocks/index.txt')

# if query passed as argument, run query
# otherwise, loop to allow user to run queries
if args.query:
    query = args.query
    result = q1.run_query(query)
    print(query + '->')
    print(result)
else:
    while True:
        query = raw_input("Enter query separated by AND | OR:")
        result = q1.run_query(query)
        print(query + '->')
        print(result)


# run_query('./blocks/index.txt', 'a')
# run_query('./blocks/index.txt', 'by')
# run_query('./blocks/index.txt', 'but')
# run_query('./blocks/index.txt', 'a AND by AND but')
# run_query('./blocks/index.txt', 'a OR by OR but')
