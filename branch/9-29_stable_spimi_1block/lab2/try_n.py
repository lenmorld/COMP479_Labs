from normalize import *

words= ['U.S.',
 'warships',
 '.',
 '``',
 'It',
 "'s",
 'removal',
 'will',
 'contribute',
 'significantly']

normalized_words = normalize(words)
pprint.pprint(normalized_words)
