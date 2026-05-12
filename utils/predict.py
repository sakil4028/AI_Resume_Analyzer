import joblib

# Load model and vectorizer
model = joblib.load('model/classifier.pkl')

vectorizer = joblib.load('model/vectorizer.pkl')


def predict_category(resume_text):

    transformed_text = vectorizer.transform([resume_text])

    prediction = model.predict(transformed_text)

    return prediction[0]