"""
CMSC 437 | PA1
ELIZA (psychotherapist machine)

Rin Pereira
Due Date: 2/2/26

Problem: Conversating with a human patient in a psychotherapy setting.
ie. How are you feeling?
ie. I'm feeling sad.
ie. Why are you feeling sad?
etc etc.

Algorithm:
* basically read in what the user says
* match it with any keywords in a while True loop
* if it matches, output that value
* ^ if it doesn't match, have a placeholder phrase like "can you say that in a different way" or refer back to a previous conversation [ELIZA goal in
the past]
* keep going and let the user be able to quit anytime by saying bye or quit
"""

import sys
import re
import random
from collections import defaultdict

def tokenize(text):
    """
    Lowercases, separates punctuation into tokens, and splits into sentences.
    """
    text = text.lower()
    # Regex: finds words/numbers OR specific punctuation marks
    tokens = re.findall(r"[\w']+|[.,!?;]", text)
    
    sentences = []
    current_sentence = []
    terminators = {'.', '!', '?'}
    
    for token in tokens:
        current_sentence.append(token)
        if token in terminators:
            sentences.append(current_sentence)
            current_sentence = []
    
    # Add last sentence if it didn't end with punctuation
    if current_sentence:
        sentences.append(current_sentence)
    return sentences

def build_model(sentences, n):
    """
    Creates a dictionary mapping (n-1) tokens to a list of successor tokens.
    """
    model = defaultdict(list)
    starts = [] # To keep track of valid sentence starters
    
    for sent in sentences:
        if len(sent) < n:
            continue
        
        # The first (n-1) tokens are a valid way to start a generated sentence
        starts.append(tuple(sent[:n-1]))
        
        for i in range(len(sent) - n + 1):
            gram = tuple(sent[i:i+n-1])
            next_token = sent[i+n-1]
            model[gram].append(next_token)
            
    return model, starts

def generate_sentence(model, starts, n):
    """
    Generates a single sentence until a terminator is reached.
    """
    curr = random.choice(starts)
    sentence = list(curr)
    terminators = {'.', '!', '?'}
    
    # Max limit of 50 to prevent infinite loops if model is sparse
    for _ in range(50):
        options = model.get(tuple(curr))
        if not options:
            break
            
        next_word = random.choice(options)
        sentence.append(next_word)
        
        if next_word in terminators:
            break
            
        curr = sentence[-(n-1):]
        
    return " ".join(sentence)

def main():
    if len(sys.argv) < 4:
        print("Usage: python ngram.py n m input_file1 [input_file2 ...]")
        return
    n = int(sys.argv[1])
    m = int(sys.argv[2])
    file_names = sys.argv[3:]

    print(f"This program generates random sentences based on an {n}-gram model.")
    print(f"Author: [Your Name]")
    print(f"Command line settings : ngram.py {n} {m}")
    print("-" * 30)

    all_sentences = []
    
    # Processing multiple files
    for file_name in file_names:
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
                all_sentences.extend(tokenize(content))
        except FileNotFoundError:
            print(f"Error: File {file_name} not found.")

    # Build the N-gram model
    model, starts = build_model(all_sentences, n)

    if not starts:
        print("Not enough data to generate sentences for that N value.")
        return

    # Generate m sentences
    for _ in range(m):
        print(generate_sentence(model, starts, n))

if __name__ == "__main__":
    main()