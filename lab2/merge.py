def intersect(blk1, vblk2):
    while blk1 != {} and blk2 != {}:
        term1 = getTerm(blk1)
        term2 = getTerm(blk2)

        if term1 == term2
            pos = merge_posting
            add (term1, pos)

			term1 = nextTerm(blk1)
			term2 = nextTerm(blk2)
        else if term1 < term2
            add (term1, pos)
            term1 = nextTerm(blk1)
        else
            add (term2, pos)
            term2 = nextTerm(blk2)
