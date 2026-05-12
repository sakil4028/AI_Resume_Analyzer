import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


df = pd.read_csv("datasets/resume_dataset.csv")


print(df.head())


X = df['Resume']

y = df['Category']


vectorizer = TfidfVectorizer(
    stop_words='english',
    max_features=5000
)

X_vectorized = vectorizer.fit_transform(X)


X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y,
    test_size=0.2,
    random_state=42
)


model = LogisticRegression()

model.fit(X_train, y_train)


y_pred = model.predict(X_test)


accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)


joblib.dump(model, 'model/classifier.pkl')


joblib.dump(vectorizer, 'model/vectorizer.pkl')

print("Model Saved Successfully")