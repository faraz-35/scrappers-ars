import nltk 
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
from nltk.tokenize import RegexpTokenizer
from collections import Counter 
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import joblib



def clean_data(text):
   # Normalizing the text
  try:
    cleaned_text = re.sub(r"[^a-zA-Z]", " ", str(text).lower())
  except:
    cleaned_text = str(text).lower()
  tokens = word_tokenize(cleaned_text)  # Tockenizing the text
  stop_words = stopwords.words("english") 
  token_words = [t for t in tokens if t not in stop_words]  # Removing the stopwords from the text
  final_text = [WordNetLemmatizer().lemmatize(w) for w in token_words]  # Converting words in their base form via lammitization
  return final_text
joblib_file = "joblib_model.pkl"
joblib_model = joblib.load(joblib_file)
joblib_vec = joblib.load('vectorizer.pkl')
# Passing the data to the loaded model for prediction
def classify_articles(article):
  fin_text = clean_data(article)
  data = ' '.join(fin_text)
  final_text = joblib_vec.transform([data])
  predict = joblib_model.predict(final_text)
  pred_category = predict[0]
  return pred_category
# print("Article's Category is :",classify_articles("I have the same problem as Romelu but mine is the left ankle, Federico Pastorello tells Sky Sports News as he also shows us the scrapes on his hands from a running injury."))