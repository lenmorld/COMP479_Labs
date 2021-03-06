import sgmllib
import string
import re


# http://www.programcreek.com/python/example/837/sgmllib.SGMLParser
# http://effbot.org/librarybook/sgmllib.htm

class FoundTitle(Exception):
    pass

class FoundBody(Exception):
    pass

class ExtractTitle(sgmllib.SGMLParser):

    def __init__(self, verbose=0):
        sgmllib.SGMLParser.__init__(self, verbose)
        self.title = self.data = None

    def handle_data(self, data):
        if self.data is not None:
            self.data.append(data)

    def start_title(self, attrs):
        self.data = []

    def end_title(self):
        self.title = string.join(self.data, "")
        raise FoundTitle # abort parsing!


class ExtractBody(sgmllib.SGMLParser):

    def __init__(self, verbose=0):
        sgmllib.SGMLParser.__init__(self, verbose)
        self.body = self.data = None

    def handle_data(self, data):
        if self.data is not None:
            self.data.append(data)

    def start_body(self, attrs):
        self.data = []

    def end_body(self):
        self.body = string.join(self.data, "")
        raise FoundBody # abort parsing!

def extract(file):
    # extract title from an HTML/SGML stream
    p = ExtractTitle()
    b = ExtractBody()
    try:
        while 1:
            # read small chunks
            s = file.read(1024)
            if not s:
                break
            b.feed(s)
        b.close()
    except FoundBody:
        return b.body
    print None



#
# try it out

# print "sgml", "=>",

lines = extract(open("./reut2-021.sgm"))
print(lines)
tokens = re.split('\s|(?<!\d)[,.](?!\d)', lines)
print(tokens)
