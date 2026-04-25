# wsd.py
# rin pereira
# mar 16 2026

# word sense disambiguation using decision list classification.

# usage: 
# python3 wsd.py line-train.txt line-test.txt my-model.txt > my-line-answers.txt

# this program learns a model from training data and predicts sense (phone | product) for each instance of word 'line' in test data.

# parse -> extract -> rank -> predict
# import re module for re.findall(r'senseid="(\w+)"', line)
# get text for each sense

# bag of words
# count how often each word (feature) appears in each sense.
# create frequency map: * Count(word, sense_phone)
# Count(word, sense_product)
# constraints: only use words found in line-train.txt

# algorithm:
# 1. parse training instances
# 2. extract bag-of-words features from contexts
# 3. count word frequencies fore ach sense
# 4. calculate log likelihood:
# log2( P(word|phone) / P(word|product) )
# 5. rank features to create a decision list
# 6. apply decision list to test sentences
# 7. if no feature fires -> use most frequent sense baseline

# decision list classifier

import sys
import re
import math
from collections import defaultdict

# step 1: read arguments
# open file
train_file = sys.argv[1]
test_file = sys.argv[2]
model_file = sys.argv[3]

# step 2: parse training data

with open(train_file) as f:
    content = f.read()

# finds every "instance" block in the file
instances = re.findall(r'<instance id="([^"]+)">(.*?)</instance>', content, re.S)

phone_counts = defaultdict(int)
product_counts = defaultdict(int)

total_phone = 0
total_product = 0

for inst_id, inst_body in instances:
    # use a variable to store the search result first
    sense_match = re.search(r'senseid="(.*?)"', inst_body)
    context_match = re.search(r'<context>(.*?)</context>', inst_body, re.S)

    # only keep going if we actually found both
    if sense_match and context_match:
        sense = sense_match.group(1)
        context = context_match.group(1)

        # cleaning code
        words = re.findall(r'\b[a-z]+\b', context.lower())

        # put words into jar
        if sense == "phone": 
            total_phone += 1
            for w in words:
                phone_counts[w] += 1
        elif sense == "product":
            total_product += 1
            for w in words:
                product_counts[w] += 1

# step 3: build feature list
total_phone_words = sum(phone_counts.values())
total_product_words = sum(product_counts.values())
vocab = set(phone_counts.keys()) | set(product_counts.keys())
decision_list = []
for word in vocab: 
    phone = (phone_counts[word] + 1) / (total_phone_words + len(vocab))
    product = (product_counts[word] + 1) / (total_product_words + len(vocab))
    score = math.log2(phone / product)
    if score > 0:
        sense = "phone"
    else:
        sense = "product"
    decision_list.append((abs(score), word, sense, score))

# step 4: sort decision list
decision_list.sort(reverse=True)

#step 5: write model file
with open(model_file, "w") as m:
    for score_abs, word, sense, score in decision_list:
        m.write(f"{word}\t{sense}\t{score}\n")

# step 6 :classify test data
with open(test_file) as f:
    test = f.read()
test_instances = re.findall(r'<instance id="([^"]+)">(.*?)</instance>', test, re.S)
baseline = "phone" if total_phone > total_product else "product"
for inst_id, inst_body in test_instances:
    context_match = re.search(r'<context>(.*?)</context>', inst_body, re.S)
    if context_match:
        context = context_match.group(1)
        words = set(re.findall(r'\b[a-z]+\b', context.lower()))
        prediction = None
        for score_abs, word, sense, score in decision_list:
            if word in words:
                prediction = sense
                break
        if prediction is None:
            prediction = baseline
        print(f'<answer instance="{inst_id}" senseid="{prediction}"/>')