from normalize import *
import nltk
from nltk.corpus import stopwords
import re
import pprint
import string

# normalizes the passed list of words by
# 1. case-folding - convert all to lowercase
# 2. remove stop words


def remove_weird_things(words):         # remove punctuations, line breaks, whitespace, etc
    punctuations = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'

    processed_words = [ t.translate(None, punctuations) for t in words ]  # remove punctuations
    garbage_words = ['','s']
    processed_words = [ t for t in processed_words if t not in garbage_words ]
    return processed_words

def remove_numbers(words):
    processed_words = [w for w in words if not w.isdigit() ]
    return processed_words

##def case_folding(dict_terms):
##    # input are plain tokens, Tree:4, tree:5  -> tree:4, tree:5
##    for token in dict_terms:
##        token["term"] = token["term"].lower()
##
##    return dict_terms

def case_folding(words):
    processed_words = [w.lower() for w in words ]
    return processed_words

def remove_stop_words(words):
    stops = set(stopwords.words("english"))
    processed_words = [w for w in words if w not in stops]
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
