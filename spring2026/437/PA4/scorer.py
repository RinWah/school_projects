import sys
import re

# scorer

def load(file_path):
    d = {}
    # try other encodings
    encodings = ['utf-8', 'utf-16', 'cp1252']
    content = None
    
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                content = f.read()
                # If we read it and find tags, we found the right encoding
                if 'instance=' in content:
                    break
        except:
            continue

    if not content:
        print(f"CRITICAL: Could not read {file_path} or file is empty.")
        return d

    # split up into lines to parse
    lines = content.splitlines()
    for line in lines:
        # flexible regex handles single/double quotes and spaces
        inst = re.search(r'instance=["\']([^"\']+)["\']', line)
        sense = re.search(r'senseid=["\']([^"\']+)["\']', line)

        if inst and sense:
            d[inst.group(1)] = sense.group(1)

    print(f"Loaded {len(d)} items from {file_path}")
    return d

if len(sys.argv) < 3:
    print("Usage: python scorer.py my-answers.txt line-key.txt")
    sys.exit(1)

answers_file = sys.argv[1]
key_file = sys.argv[2]

pred = load(answers_file)
gold = load(key_file)

print(f"Summary: Predictions={len(pred)}, Gold={len(gold)}")

correct = 0
confusion = {
    "phone": {"phone": 0, "product": 0},
    "product": {"phone": 0, "product": 0}
}

# only score if we have predictions
if len(pred) == 0:
    print("ERROR: No predictions found in the answer file. Accuracy cannot be calculated.")
else:
    for inst in gold:
        g = gold[inst]
        p = pred.get(inst)
        
        if p == g:
            correct += 1
        
        if p in confusion[g]:
            confusion[g][p] += 1
        else:
            # handle cases where model might predict unexpected label
            pass

    accuracy = correct / len(gold)
    print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print("\nConfusion Matrix:")
    print(confusion)