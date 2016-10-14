from collections import OrderedDict
import ast

class QueryObject:

    def __init__(self, index_file):
        self.index  = read_index_into_memory(index_file)

    @staticmethod
    def query_list(index, term_list, op):


        if len(term_list) >1:
            # get postings of first term
            and_postings = index[term_list[0]]                 # used for plaing and-ing of documents
            and_postings_multiple = [index[term_list[0]], ]    # accumulate intersection of documents per level ,e.g 1 doc, 2 docs 'and-ed', 3 docs 'and-ed', ...
            or_postings = index[term_list[0]]

            #### doing OR with priority on the Intersections ###
            # to process OR, we need to order documents by how many keywords they contains
            # e.g. for a 3 word query, the first in the list should be the ones that contain all 3 keywords (i.e. the intersection of all 3)
            #       then the intersection of just 2 docs, and lastly the other docs that has either of the 3 but no intersection
            # to do that, we have to know the intersection at each level, in which level means incresing number of documents we are intersecting

            docs_processed_ctr = 0
            for t in term_list:
                and_postings = list(set(and_postings) & set(index[t]))
                and_postings_multiple.insert(0, and_postings)           # add the intersection of this much documents to the head of the list
                                                                        # at the end of the loop, we will have the intersection of all (or most) docs at the start of the list
                or_postings = list(set(or_postings) | set(index[t]))
            if op == 'AND':
                return and_postings
            elif op == 'OR':
                # we want to put first the ones that have their intersection
                list_collector = []
                for and_postings_m in and_postings_multiple:        # go through all intersections, starting with the most 'encompassing' one
                    for item in and_postings_m:                     # for each intersection, get the list items
                        if item not in list_collector:              # instead of simply appending which will cause duplicates (and forced ordering for sets)
                            list_collector.append(item)             # we carefully append to the end of the final list, if item is not there yet
                return list_collector

        else:
            return self.index[term_list]



    def run_query(self, query):
        # index  = read_index_into_memory(index_file)
        # print(index)
        index = self.index
        q_split = query.split()

        if len(q_split) == 1:
            # single word query
            result = index[query]
        else:
            if 'AND' in query:
                # multiple words query - cat AND dog
                q_terms = query.split(' AND ')
                result = QueryObject.query_list(index, q_terms, 'AND')
            elif 'OR' in query:
                # multiple words query - cat OR dog
                q_terms = query.split(' OR ')
                result = QueryObject.query_list(index, q_terms, 'OR')

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
    # print(len(index))
    return index



# run_query('./blocks/index.txt', 'a')
# run_query('./blocks/index.txt', 'by')
# run_query('./blocks/index.txt', 'but')
# run_query('./blocks/index.txt', 'a AND by AND but')
# run_query('./blocks/index.txt', 'a OR by OR but')
