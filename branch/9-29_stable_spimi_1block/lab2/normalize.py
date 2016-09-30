from nltk.corpus import stopwords
import re
import pprint


# normalizes the passed list of words by
# 1. case-folding - convert all to lowercase
# 2. remove stop words
def normalize(words):
    """
    :param words: words text
    :return: normalized text according to: Alec Go (2009)'s Twitter Sentiment Classification using Distant Supervision
    """
    # http://stackoverflow.com/questions/2304632/regex-for-twitter-username

    empty_words = ['',' ','``','.',"'s",',','\x03',"''"]
    stops = set(stopwords.words("english"))
    new = []
    for word in words:
        word = word.lower()
        new.append(word)
        
    tokens = [w for w in new if ((not w in stops) and (not w in empty_words)  )]

    #print("---words---")
    #pprint.pprint(tokens)
    #x = raw_input("PAUSE")
    

    return tokens
    
