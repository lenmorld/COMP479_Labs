a = []

def meth(x):
    a.append('a') if x < 1 else a.append('c')

meth(3)
print(a)
