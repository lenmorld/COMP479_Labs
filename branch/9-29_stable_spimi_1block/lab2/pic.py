try: import cPickle as pickle
except: import pickle
import pprint


dict1 = {u'--': [3],
 u'astrid': [3],
 u'beacon': [3],
 u'blown': [3],
 u'christma': [3],
 u'dot': [3],
 u'gulf': [3],
 u'huge': [3],
 u'like': [3],
 u'lit': [3],
 u'monday': [3],
 u'night': [3],
 u'offshor': [3],
 u'oil': [3],
 u'oilfield': [3],
 u'one': [3],
 u'platform': [3],
 u'reuter': [3],
 u'rostam': [3],
 u'sit': [3],
 u'tree': [3],
 u'u.': [3],
 u'usual': [3],
 u'warship': [3],
 u'water': [3]}


dict2 = {u'action': [1],
 u'ask': [1],
 u'confront': [1],
 u'contribut': [1],
 u'countermeasur': [1],
 u'escal': [1],
 u'escort': [1],
 u'forc': [1],
 u'futur': [1],
 u'gulf': [1],
 u'iran': [1],
 u'meet': [1],
 u'militari': [1],
 u"navy'": [1],
 u'oil': [1],
 u'oper': [1],
 u'prepar': [1],
 u'remov': [1],
 u'reuter': [1],
 u'safeti': [1],
 u'said': [1],
 u'seek': [1],
 u'significantli': [1],
 u'state': [1],
 u'stronger': [1],
 u'tanker': [1],
 u'u.s.': [1],
 u'unit': [1],
 u'warship': [1],
 u'weinberg': [1]}

with open('file1.bin','wb') as file1:
    pickle.dump(dict1,file1)
    pickle.dump(dict2,file1)
print('after')
with open('file1.bin','rb') as file1:
    data1 = pickle.load(file1)
    data2 = pickle.load(file1)

pprint.pprint(data1)
pprint.pprint(data2)



