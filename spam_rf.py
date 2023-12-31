import numpy as np
import pandas as pd
import re
import nltk
nltk.download('wordnet')
from sklearn.datasets import load_files
nltk.download('stopwords')
nltk.download('omw-1.4')
import pickle
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.ensemble import RandomForestClassifier

def spam_clasificador(mensaje, modelo):
    mssgdata = pd.read_csv('spam.csv', encoding='latin-1')
    X, y = mssgdata.v2, mssgdata.v1
    X = pd.Series(np.concatenate((X, [mensaje])))
    documents = []

    from nltk.stem import WordNetLemmatizer

    stemmer = WordNetLemmatizer()

    for sen in range(0, len(X)):
        document = re.sub(r'\W', ' ', str(X[sen]))
        document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
        document = re.sub(r'\^[a-zA-Z]\s+', ' ', document) 
        document = re.sub(r'\s+', ' ', document, flags=re.I)
        document = re.sub(r'^b\s+', '', document)
        document = document.lower()
        document = document.split()

        document = [stemmer.lemmatize(word) for word in document]
        document = ' '.join(document)
        
        documents.append(document)
        
    vectorizer = CountVectorizer(max_features=10000, min_df=1, max_df=0.6, ngram_range=(1,2), stop_words=stopwords.words('english'))
    X = vectorizer.fit_transform(documents).toarray()

    tfidfconverter = TfidfTransformer()
    X = tfidfconverter.fit_transform(X).toarray()

    y_p = modelo.predict(X[-1].reshape(1, -1))

    return y_p