try: import cPickle as pickle
except: import pickle
import pprint

file1= open('block.bin','rb')
data2 = pickle.load(file1)
pprint.pprint(data2)



