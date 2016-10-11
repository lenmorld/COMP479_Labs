from os import listdir
from os.path import isfile, join


def get_reuter_files(doc_path):

    only_files = [f for f in listdir(doc_path) if isfile(join(doc_path, f))]
    reuter_files = [f for f in only_files if f.endswith('.sgm')]

    # print(reuter_files)
    return reuter_files
