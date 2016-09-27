from string import ascii_uppercase,ascii_lowercase,digits
from random import choice
try: from cPickle import HIGHEST_PROTOCOL,dump,load
except: from pickle import HIGHEST_PROTOCOL,dump,load
from sys import argv

with open("".join(choice(ascii_uppercase+ascii_lowercase+digits) for _ in xrange(10))+".bin","wb") as output_file:
    output_file.write('haha')
output_file.close()
