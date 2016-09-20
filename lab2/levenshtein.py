# levenshtein algo

import pprint

# load 2-d matrix



def load_matrix(s1, s2):
    y= len(s2)+1
    x = len(s1)+1

    m = [[0] * y for i in range(x)]
    print('matrix init')
    pprint.pprint(m)
    for i in range(x):
        m[i][0] = i
    for j in range(y):
        m[0][j] = j
    print('matrix after index load')
    pprint.pprint(m)


    print(x)
    print(y)
    for i in range(1, x):
        for j in range(1, y):
            print i, ' ', j, ' ', m[i][j]
        
            if s1[i] == s2[j]:
                m[i][j] = min((m[i-1][j])+1, m[i][j-1]+1, m[i-1][j-1])
            else:
                m[i][j] = min((m[i-1][j])+1, m[i][j-1]+1, (m[i-1][j-1])+1)

    x = len(s1)
    y = len(s2)
    print('x:' + str(x))
    print('y:' + str(y))
    print(m[x][y])
    return m

print("Distance:")
matrix = load_matrix('cats','fast')
print("---- final matrix --------")
pprint.pprint(matrix)
