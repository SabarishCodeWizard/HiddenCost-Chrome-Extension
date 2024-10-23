import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import BernoulliNB
from sklearn import metrics
from joblib import dump
import matplotlib.pyplot as plt
# import seaborn as sns

# Load datasets
df1 = pd.read_csv('normie.csv')
df2 = pd.read_csv('dark_patterns.csv')

# Preprocess df1
df1 = df1[pd.notnull(df1["Pattern String"])]
df1 = df1[df1["classification"] == 0]
df1["classification"] = "Not Dark"
df1.drop_duplicates(subset="Pattern String", inplace=True)

# Preprocess df2
df2 = df2[pd.notnull(df2["Pattern String"])]
df2["classification"] = "Dark"
col = ["Pattern String", "classification"]
df2 = df2[col]

# Combine datasets
df = pd.concat([df1, df2])

# Add additional features
df['Pattern Length'] = df['Pattern String'].apply(len)  # Length of the pattern string
df['Pattern Word Count'] = df['Pattern String'].apply(lambda x: len(x.split()))  # Word count
df['Average Word Length'] = df['Pattern String'].apply(lambda x: sum(len(word) for word in x.split()) / len(x.split()) if len(x.split()) > 0 else 0)  # Average word length

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    df['Pattern String'], df["classification"], train_size=0.25, random_state=42)

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

# Train the classifier
clf = BernoulliNB().fit(X_train_tfidf, y_train)

# Predict and evaluate
y_pred = clf.predict(count_vect.transform(X_test))
print("Accuracy: ", metrics.accuracy_score(y_pred, y_test))

# Optional: Uncomment to plot confusion matrix
# conf_mat = confusion_matrix(y_test, y_pred)
# fig, ax = plt.subplots(figsize=(10,10))
# sns.heatmap(conf_mat, annot=True, fmt='d')
# plt.ylabel('Actual')
# plt.xlabel('Predicted')
# plt.show()

# Save the trained model and vectorizer
dump(clf, 'presence_classifier.joblib')
dump(count_vect, 'presence_vectorizer.joblib')
