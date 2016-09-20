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

    
    stops = set(stopwords.words("english"))
    
    for word in words:
        word = word.lower()  
        word = re.sub('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', 'USER', word)
        word = word.replace('\\', '')
        word = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 'URL', word)

    tokens = [w for w in words if (not w in stops)]    

    return tokens
    
