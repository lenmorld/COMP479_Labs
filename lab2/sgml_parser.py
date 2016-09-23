import sgmllib
import string
import re
import pprint


# http://www.programcreek.com/python/example/837/sgmllib.SGMLParser
# http://effbot.org/librarybook/sgmllib.htm

class FoundTitle(Exception):
    pass

class FoundBody(Exception):
    pass

##class ExtractTitle(sgmllib.SGMLParser):
##
##    def __init__(self, verbose=0):
##        sgmllib.SGMLParser.__init__(self, verbose)
##        self.title = self.data = None
##
##    def handle_data(self, data):
##        if self.data is not None:
##            self.data.append(data)
##
##    def start_title(self, attrs):
##        self.data = []
##
##    def end_title(self):
##        self.title = string.join(self.data, "")
##        raise FoundTitle # abort parsing!


class ExtractText(sgmllib.SGMLParser):

    contents = {}
    reuterAll = 3   # number of body inside the file
    reuterCtr = 0

    def __init__(self, verbose=0):
        sgmllib.SGMLParser.__init__(self, verbose)
        self.body = self.data = None

    def handle_data(self, data):
        if self.data is not None:
            self.data.append(data)

    def start_title(self, attrs):
        self.data = []

    def end_title(self):
        self.title = string.join(self.data, "")
        #print(self.title)
        self.contents[self.title] = ''

    def start_body(self, attrs):
        self.data = []

    def end_body(self):
        self.body = string.join(self.data, "")
        self.contents[self.title] = self.body
        self.reuterCtr += 1
        print self.reuterCtr
        
        if self.reuterCtr == self.reuterAll:   
            raise FoundBody # abort parsing!

def extract(file):
    dict_term = {}
    ctr = 0
    
    while True:     
    
        # extract title from an HTML/SGML stream
        b = ExtractText()

##        if p is None:
##            break
##        if b is None:
##            break
##        
        try:
            while 1:
                # read small chunks
                s = file.read(1024)
                if not s:
                    break
                b.feed(s)
            b.close()
        except FoundBody:
            return b.contents
            #return b.body
            #a = raw_input()
            #preface = b.body[:100]      # get first 100 char as key
            #dict_term[preface] =  b.body
            #print(docs[ctr])
            ctr += 1
    return docs



#docs = extract(open("./reut2-021.sgm"))
#pprint.pprint(docs)




