import re
import nltk
import spacy

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nlp = spacy.load("en_core_web_sm")

stop_words = set(stopwords.words('english'))

lemmatizer = WordNetLemmatizer()


def clean_text(text):

    text = text.lower()

    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)

    text = re.sub(r'\s+', ' ', text)

    return text


def preprocess_text(text):

    cleaned_text = clean_text(text)

    tokens = word_tokenize(cleaned_text)

    filtered_tokens = []

    for word in tokens:

        if word not in stop_words and len(word) > 2:

            lemma = lemmatizer.lemmatize(word)

            filtered_tokens.append(lemma)

    return filtered_tokens


def extract_named_entities(text):

    doc = nlp(text)

    entities = []

    for ent in doc.ents:
        entities.append((ent.text, ent.label_))

    return entities