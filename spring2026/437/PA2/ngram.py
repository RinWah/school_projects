# i need a program that has a method/function with params of n [# in ngram], m [number of sentences], file.txt [file that we are processing to get ngrams from]
# method needs
# convert to lowercase
# separate OR remove punctuation
# identify sentence endings, only . ! ?
from sys import argv # for the lists
import re # for regex

# avoid "end. once" bigrams

# needs file input within function, let's say it's called texts
def processor():
    # read file
    document = open("demofile.txt")
    # convert to lowercase, don't considerably know where this is to go yet.
    document.lower()
    read_in = string(argv[1:])
    processor(document, read_in, texts)


    # separate / remove punctuation
    # regex pattern: r"\w+|[.!?,]"

    # do some fancy slicing to get rid of the punctuation and/or separate characters/tokens.
    split(argv) # i don't remember the args T_T
    re.findall(r"\w+|[.!?,]", argv)

    # \w+ = matches one word characters
    # | OR
    # [.!?,] = punctuation
    # identify sentences
    # make bigrams
    # generate sentences

def main():
    # file read in process
    
    processor()
