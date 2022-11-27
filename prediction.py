import nltk
import re
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf

from nltk.stem.porter import PorterStemmer ##stemming purpose
from nltk.stem import WordNetLemmatizer #lemmatization purpose
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

from constants import VOC_SIZE, SENT_LENGTH

ps = PorterStemmer()
lemmatizer=WordNetLemmatizer()

model = tf.keras.models.load_model('models/lstm_model')

def preprocess(s_input):
    review = re.sub("[^a-zA-Z]", " ", s_input)
    review = review.lower()
    review = review.split()
    review = [lemmatizer.lemmatize(word) for word in review if not word in stopwords.words('english')] 
    review = ' '.join(review)

    # words to number
    one_hot_rep = one_hot(review,VOC_SIZE)

    # padding
    embedded_review = pad_sequences([one_hot_rep],padding='post',maxlen=SENT_LENGTH)
    return embedded_review


def predict_sentiment(input):
    processed_input = preprocess(input)
    pred=model.predict(processed_input)
    return pred[0][0]

# print(predict_sentiment("I love this movie"))