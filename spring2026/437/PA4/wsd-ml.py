import sys
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier 
from sklearn.svm import LinearSVC

# handle CL args
train_file = sys.argv[1]
test_file = sys.argv[2]
# if there's a 3rd arg, use that, otherwise default to NaiveBayes
model_name = sys.argv[3] if len(sys.argv) > 3 else "NaiveBayes"
# parse training file
with open(train_file, 'r') as f:
    train_content = f.read()

train_instance = re.findall(r'<instance id="([^"]+)">(.*?)</instance>', train_content, re.S)
train_contexts = []
train_labels = []

for inst_id, inst_body in train_instances:
    sense_match = re.search(r'senseid="(.*?)"', inst_body)
    context_match = re.search(r'<context>(.*?)</context>', inst_body, re.S)
    if sense_match and context_match:
        train_labels.append(sense_match.group(1))
        # clean text -> lowercase & get rid of punctuation
        clean_text = " ".join(re.findall(r'\b[a-z]+\b', context_match.group(1).lower()))
        train_contexts.append(clean_text)
# bow
# initialize
# features from training data
vectorizer = CountVectorizer()
# learn vocab & transform training data
X_train = vectorizer.fit.transform(train_contexts)
# choose model
if model_choice == "DecisionTree":
    clf = DecisionTreeClassifier()
elif model_name == "SVM":
    clf = LinearSVC()
else: # default naivebayes
    clf = MultinomialNB()
clf.fit(X_train, train_labels)
# parse & classify test data
with open(test_file, 'r') as f:
    test_content = f.read()
test_instances = re.findall(r'<instance id="([^"]+)">(.*?)</instance>', test_content, re.S)
for inst_id, inst_body in test_instances:
    context_match = re.search(r'<context>(.*?)')