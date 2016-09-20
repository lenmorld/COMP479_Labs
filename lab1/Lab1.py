import nltk, pprint
from sgmllib import SGMLParser
# from io import StringIO
# from lxml import etree

# dtd.elements()[0].content.right.left

sgml = SGMLParser()

with open('./reut2-021.sgm','r') as f:
     list1 = f.read().splitlines()
     sgml.feed(str(list1))
     print(sgml)
sgml.close()

