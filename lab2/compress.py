from normalize import *
import nltk
from nltk.corpus import stopwords
import re
import pprint

# normalizes the passed list of words by
# 1. case-folding - convert all to lowercase
# 2. remove stop words



def remove_numbers(words):
    processed_words = [w for w in words if not w.isdigit() ]
    return processed_words

def remove_stop_words(words):
    stops = set(stopwords.words("english"))
    processed_words = [w for w in words if (not w in stops)]
    return processed_words


def remove_non_words():
    pass
    # empty_words = ['',' ','``','.',"'s",',','\x03',"''"]

def normalize(words):
    pass
    # empty_words = ['',' ','``','.',"'s",',','\x03',"''"]
    #
    # new = []
    # for word in words:
    #     word = word.lower()
    #     new.append(word)
    #
    # #normalized_words = [w for w in new if ((not w in stops) and (not w in empty_words)  )]
    #
    # #print("NORMALIZE---------------------------")
    # #pprint.pprint(normalized_words)
    # return normalized_words

def p_stemmer(terms):
    stemmer = PorterStemmer()
    stemmed_terms = [stemmer.stem(term) for term in terms]

    return stemmed_terms

    # print("STEMMER---------------------------")
    # pprint.pprint(stemmed_terms)
