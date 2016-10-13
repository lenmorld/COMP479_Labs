# from contextlib import contextmanager
import filestuff
#
# block_path = './blocks/'
#
# @contextmanager
# def multi_file_manager(doc_path, files, mode='rt'):
#     files = [open(doc_path + file, mode) for file in files]
#     yield files
#     for file in files:
#         file.close()
#
# filenames = filestuff.get_files(block_path, '.txt')
#
# with multi_file_manager(block_path, filenames) as files:
#     f1 = files[0]
#     f2 = files[1]

import linecache

block_path = './blocks'
filenames = filestuff.get_files(block_path, '.txt')
block_count = len(filenames)

for f in filenames:
    print(linecache.getline(f, 2))



    # for f in files:
    #     ctr = 0
    #     for line in f:
    #         print line
    #         ctr += 1
    #
    #         if ctr == 5:
    #             break

#with open('block1.txt') as f:
#        for line in f:
#            print line



# def intersect(blk1, vblk2):
#     while blk1 != {} and blk2 != {}:
#         term1 = getTerm(blk1)
#         term2 = getTerm(blk2)
#
#         if term1 == term2
#             pos = merge_posting
#             add (term1, pos)
#
# 			term1 = nextTerm(blk1)
# 			term2 = nextTerm(blk2)
#         else if term1 < term2
#             add (term1, pos)
#             term1 = nextTerm(blk1)
#         else
#             add (term2, pos)
#             term2 = nextTerm(blk2)
