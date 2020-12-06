import wget
from os import mkdir
from shutil import rmtree

with open('datasets.txt') as datasets_file:
    urls = datasets_file.readlines()

    if len(urls) > 5:
        raise Exception("Too many datasets were specified")

    rmtree('datasets', ignore_errors=True)
    mkdir('datasets')

    for u in urls:
        f = wget.download(u.rstrip(), 'datasets/')
        print(f)