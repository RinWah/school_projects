# parse -> extract -> rank -> predict
# import re module for re.findall(r'senseid="(\w+)"', line)
# get text for each sense

# bag of words
# count how often each word (feature) appears in each sense.
# create frequency map: * Count(word, sense_phone)
# Count(word, sense_product)
# constraints: only use words found in line-train.txt

# decision list classifier
