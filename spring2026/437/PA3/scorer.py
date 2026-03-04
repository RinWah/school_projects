import sys
import re
import random

def main(): 
    with open("line-test.txt", "r") as f:
        test = f.read()
    with open("line-train.txt", "r") as f:
        train = f.read()
    accuracy = 0
    confusion_matrix = []
    