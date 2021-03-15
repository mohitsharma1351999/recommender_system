import nltk
from nltk.corpus import stopwords
import pandas as pd
from nltk.stem import PorterStemmer
from tqdm import tqdm

news_csv = pd.read_csv('data.csv', encoding='latin1')

#removing non-ascii characters
for i in range (0 , news_csv.shape[0]):
    news_csv['Title'][i]=(news_csv['Title'][i].encode('ascii', 'ignore')).decode("utf-8")
    news_csv['Synopsis'][i]=(news_csv['Synopsis'][i].encode('ascii', 'ignore')).decode("utf-8")
    news_csv['News'][i]=(news_csv['News'][i].encode('ascii', 'ignore')).decode("utf-8")

#converting to lower case
news_csv['Title'] = news_csv['Title'].str.lower()
news_csv['Synopsis'] = news_csv['Synopsis'].str.lower()
news_csv['News'] = news_csv['News'].str.lower()

# 1) Tokenization: the process of segmenting text into words, clauses or sentences (here we will separate out words and remove punctuation).
# 2) Stemming: reducing related words to a common stem.
# 3) Removal of stop words: removal of commonly used words unlikely to be useful for learning.
stemming = PorterStemmer()
stops = set(stopwords.words("english"))                  

for i in tqdm(range (0 , news_csv.shape[0])):
    title = news_csv['Title'][i]
    title_tokens = nltk.word_tokenize(title)
    # taken only words (not punctuation)
    title_token_words = [w for w in title_tokens if w.isalnum()]
    title_stemmed_list = [stemming.stem(word) for word in title_token_words]
    title_meaningful_words = [w for w in title_stemmed_list if not w in stops]
    news_csv['Title'][i] = ( " ".join(title_meaningful_words))
    
    synopsis = news_csv['Synopsis'][i]
    synopsis_tokens = nltk.word_tokenize(synopsis)
    # taken only words (not punctuation)
    synopsis_token_words = [w for w in synopsis_tokens if w.isalnum()]
    synopsis_stemmed_list = [stemming.stem(word) for word in synopsis_token_words]
    synopsis_meaningful_words = [w for w in synopsis_stemmed_list if not w in stops]
    news_csv['Synopsis'][i] = ( " ".join(synopsis_meaningful_words))
    
    news = news_csv['News'][i]
    news_tokens = nltk.word_tokenize(news)
    # taken only words (not punctuation)
    news_token_words = [w for w in news_tokens if w.isalnum()]
    news_stemmed_list = [stemming.stem(word) for word in news_token_words]
    news_meaningful_words = [w for w in news_stemmed_list if not w in stops]
    news_csv['News'][i] = ( " ".join(news_meaningful_words))





