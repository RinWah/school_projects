from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
X_train = vectorizer.transform(train_contexts)

if model_choice == "NaiveBayes":
    clf = MultinomialNB()
clf.fit(X_train, train_labels)