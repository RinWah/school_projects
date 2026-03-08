# parse -> extract -> rank -> predict
# import re module for re.findall(r'senseid="(\w+)"', line)
# get text for each sense

# bag of words
# count how often each word (feature) appears in each sense.
# create frequency map: * Count(word, sense_phone)
# Count(word, sense_product)
# constraints: only use words found in line-train.txt

# decision list classifier

import sys
import re

# open file
train_file = sys.argv[1]

with open(train_file, 'r') as f:
    content = f.read()

# finds every "instance" block in the file
instances = re.findall(r'<instance id="(.*?)">(.*?)</instance>', content, re.S)

for inst_id, inst_body in instances:
    #1. find the answer (phone or product)
    sense = re.search(r'senseid="(.*?)"', inst_body).group(1)

    #2. find the context (the sentence)
    # we want everything inside context not including the tag
    context = re.search(r'<context>(.*?)</context>', inst_body, re.S).group(1)

    #3. clean text: remove <tags>, punctuation, lowercase
