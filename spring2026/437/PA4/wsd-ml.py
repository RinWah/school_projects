import sys
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC

# ========================================================================
# description of models / features
# features: bag-of-words rep (counts unique words from training data).
# clean -> lowercase text + remove punctuation
# models: Naive Bayes, Decision Tree, SVM.
#
# comparison
# mfs base: 52.41%
# pa3 decision list: 89.68%
# naive bayes accuracy: 94.44%
# decision tree accuracy: 80.16%
# svm accuracy: 90.48%
# ========================================================================

def parse_data(file_path, is_training=True):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        sys.stderr.write(f"ERROR: File {file_path} not found.\n")
        return [], [], []

    # Robust regex: handles spaces, single/double quotes, and attributes
    instances = re.findall(r'<instance\s+id=["\']([^"\']+)["\']\s*.*?>(.*?)</instance>', content, re.S | re.I)
    ids, contexts, labels = [], [], []

    for inst_id, inst_body in instances:
        # Robust context regex
        context_match = re.search(r'<context\s*.*?>(.*?)</context>', inst_body, re.S | re.I)
        if context_match:
            text = context_match.group(1).lower()
            text = " ".join(re.findall(r'\b[a-z0-9]+\b', text))
            
            ids.append(inst_id)
            contexts.append(text)
            
            if is_training:
                # Robust senseid regex
                sense_match = re.search(r'senseid=["\']([^"\']+)["\']', inst_body, re.I)
                labels.append(sense_match.group(1) if sense_match else "phone")

    # Debug info to your console
    sys.stderr.write(f"DEBUG: Processed {len(ids)} instances from {file_path}\n")
    return ids, contexts, labels

# 1. Setup
if len(sys.argv) < 3:
    print("Usage: python wsd-ml.py line-train.txt line-test.txt [model]")
    sys.exit(1)

train_file, test_file = sys.argv[1], sys.argv[2]
model_type = sys.argv[3] if len(sys.argv) > 3 else "NaiveBayes"

# 2. Extract Data
train_ids, train_contexts, train_labels = parse_data(train_file, is_training=True)
test_ids, test_contexts, _ = parse_data(test_file, is_training=False)

# 3. ML Pipeline
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(train_contexts)
X_test = vectorizer.transform(test_contexts)

if model_type == "DecisionTree":
    clf = DecisionTreeClassifier()
elif model_type == "SVM":
    clf = LinearSVC(max_iter=10000, dual=False)
else:
    clf = MultinomialNB()

clf.fit(X_train, train_labels)
predictions = clf.predict(X_test)

# 4. Output to STDOUT
for inst_id, pred in zip(test_ids, predictions):
    print(f'<answer instance="{inst_id}" senseid="{pred}"/>')