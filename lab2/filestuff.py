from os import listdir
from os.path import isfile, join


def get_files(doc_path, file_ext):

    only_files = [f for f in listdir(doc_path) if isfile(join(doc_path, f))]
    file_types = [(doc_path + '/' +  f) for f in only_files if f.endswith(file_ext)]

    # print(reuter_files)
    return file_types


def delete_content(f_name):
    with open(f_name, "w"):
        pass
