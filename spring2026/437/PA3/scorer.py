import sys
import re

answers = sys.argv[1]
key = sys.argv[2]

def load(file):
    d = {}
    with open(file) as f:
        for line in f:
            m = re.search(r'instance="(.*?)".*senseid="(.*?)"', line)
            if m:
                d[m.group(1)] = m.group(2)
    return d

pred = load(answers)
gold = load(key)

correct = 0

confusion = {
    "phone": {"phone": 0, "product":0},
    "product": {"phone":0, "product":0}
}

for inst in gold:
    g = gold[inst]
    p = pred.get(inst)
    if p == g:
        correct += 1
    confusion[g][p] += 1

accuracy = correct / len(gold)

print("accuracy:")

def main(): 
    with open("line-test.txt", "r") as f:
        test = f.read()
    with open("line-train.txt", "r") as f:
        train = f.read()
    accuracy = 0
    confusion_matrix = []
    
    