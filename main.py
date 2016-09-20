import nltk
import json
from nltk.stem.porter import *


from normalize import *
from sgml_parser import *

# words = ['cat','dog','sleep','the']

empty_words = ['',' ']

## tokenize SGM doc to a list
lines = extract(open("../reut2-021.sgm"))
print(lines)
terms = re.split('\s|(?<!\d)[,.](?!\d)', lines)
# print(terms)
terms = [t for t in terms if (not t in empty_words)]

## normalize words
normalized_words = normalize(terms)
print("NORMALIZE---------------------------")
pprint.pprint(normalized_words)

## stemming
stemmer = PorterStemmer()
tokens = [stemmer.stem(word) for word in normalized_words]

print("STEMMER---------------------------")
pprint.pprint(tokens)







