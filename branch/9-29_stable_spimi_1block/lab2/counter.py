def count_body(file):
    f = open(file,'r')
    total = 0
    for line in f:
        if "<BODY>" in line:
            total += 1
    f.close()
    return total
