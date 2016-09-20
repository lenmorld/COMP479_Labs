# levenshtein algo

import pprint

# load 2-d matrix



def load_matrix(s1, s2):
    x = len(s1)+1
    y= len(s2)+1

    s1 = ' ' + s1
    s2 = ' ' + s2

    m = [[0] * y for i in range(x)]
    print('matrix init')
    pprint.pprint(m)
    for i in range(1,x):
        m[i][0] = i
    for j in range(1,y):
        m[0][j] = j
    print('matrix after index load')
    pprint.pprint(m)


    print(range(1,x))
    print(y)
    
    
    for i in range(1, x):
        for j in range(1, y):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1

            m[i][j] = min((m[i-1][j])+1,    # deletion
                          m[i][j-1]+1,      # insertion
                          (m[i-1][j-1])+ cost) # substitution

            print i, ',', j, ':', m[i][j], ' ', s1[i], ',', s2[j]

    print("---- final matrix --------")
    pprint.pprint(m)    

    return m[x-1][y-1]


distance = load_matrix('cats','fast')

print("Distance:")
print(distance)
