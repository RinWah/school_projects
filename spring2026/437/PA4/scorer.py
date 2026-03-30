import sys
import re

answers = sys.argv[1]
key = sys.argv[2]

def load(file):
    d = {}
    with open(file) as f:
        for line in f:
            print("LINE:", repr(line))  # debug
            inst = re.search(r'instance="([^"]+)"', line)
            sense = re.search(r'senseid="([^"]+)"', line)

            if inst and sense:
                d[inst.group(1)] = sense.group(1)

    print("Loaded:", len(d))
    return d

pred = load(answers)
gold = load(key)

print("pred size:", len(pred))
print("gold size:", len(gold))

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
    if p is None:
        continue
    confusion[g][p] += 1

accuracy = correct / len(gold)

print("accuracy:", accuracy)
print()

print("confusion matrix")
print(confusion)