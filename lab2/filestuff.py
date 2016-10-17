from os import listdir
from os.path import isfile, join
import sgml_parser


def get_files(doc_path, file_ext):

    only_files = [f for f in listdir(doc_path) if isfile(join(doc_path, f))]
    file_types = [(doc_path + '/' +  f) for f in only_files if f.endswith(file_ext)]

    # print(reuter_files)
    return file_types


def get_reuters(doc_path):
    ##### file management ##############
    # file1 = "./docs/reut2-021.sgm"
    reuter_files = get_files(doc_path, '.sgm')
    docs = {}
    for reuter_file in reuter_files:
        new_docs = sgml_parser.extract(open(reuter_file))
        docs = dict(docs.items() + new_docs.items())
    return docs


def delete_content(f_name):
    with open(f_name, "w"):
        pass
