"""
CMSC 437 | PA2
n gram sentence generator

Rin Pereira
Due Date: 2/23/26

Problem: reading in text and then generating texts that follow the same theme.

Algorithm:
* read in what the files say
* match it with associations and keywords to produce sentences that fit the context.
* after separating out punctuation.
* word association.
"""
"""
CMSC 437 | PA2
N-gram Sentence Generator
Rin Pereira
Due Date: 2/23/26
"""

import sys
import re
import random

def get_tokens(text):
    # Lowercase and split everything out
    text = text.lower()
    # Matches words, numbers, or specific punctuation
    tokens = re.findall(r"[\w']+|[.,!?;]", text)
    
    sentences = []
    temp_sent = []
    stops = {'.', '!', '?'}
    
    for t in tokens:
        temp_sent.append(t)
        if t in stops:
            sentences.append(temp_sent)
            temp_sent = []
            
    if temp_sent:
        sentences.append(temp_sent)
    return sentences

def main():
    # Basic check for command line args
    if len(sys.argv) < 4:
        print("Usage: python ngram.py n m file1 file2...")
        return

    n = int(sys.argv[1])
    m = int(sys.argv[2])
    files = sys.argv[3:]

    # Header info required by prompt
    print(f"This program generates random sentences based on an {n}-gram model.")
    print("Author: Rin Pereira")
    print(f"Command line settings : ngram.py {n} {m}")
    print("") # spacer

    all_sentences = []
    for f_name in files:
        try:
            with open(f_name, 'r', encoding='utf-8') as f:
                raw_data = f.read()
                all_sentences.extend(get_tokens(raw_data))
        except:
            print(f"Could not read file: {f_name}")

    # The N-gram dictionary
    # Key: tuple of (n-1) words, Value: list of words that follow
    ngram_map = {}
    starters = [] 

    for s in all_sentences:
        if len(s) < n:
            continue
            
        # Keep track of how sentences actually start
        starters.append(tuple(s[:n-1]))
        
        for i in range(len(s) - n + 1):
            context = tuple(s[i:i+n-1])
            target = s[i+n-1]
            
            if context not in ngram_map:
                ngram_map[context] = []
            ngram_map[context].append(target)

    # Generate the M sentences
    terminals = {'.', '!', '?'}
    for _ in range(m):
        # Pick a random starting point
        current_gram = random.choice(starters)
        output = list(current_gram)
        
        # Limit to 100 words so it doesn't loop forever
        for _ in range(100):
            if current_gram not in ngram_map:
                break
                
            possibilities = ngram_map[current_gram]
            next_word = random.choice(possibilities)
            output.append(next_word)
            
            if next_word in terminals:
                break
            
            # Slide the window forward
            current_gram = tuple(output[-(n-1):])
            
        print(" ".join(output))

if __name__ == "__main__":
    main()