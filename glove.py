import numpy as np
from nltk.corpus import stopwords
stop=set(stopwords.words('english'))
from nltk.tokenize import word_tokenize
import gensim
from keras.preprocessing.text import Tokenizer
from tqdm import tqdm
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from yellowbrick.cluster import KElbowVisualizer
import matplotlib.pyplot as plt 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import adjusted_rand_score  


def create_corpus(df):
    corpus=[]
    for news in tqdm(df['Synopsis']):
        words=[word.lower() for word in word_tokenize(news) if((word.isalpha()==1) & (word not in stop))]
        corpus.append(words)
    # Corpus: List of List of length --> [4654 X (varies , depending on the length of synopsis)]
    return corpus


def pre_trainModel():
    embedding_dict={}
    #pre-trained Model : glove.6B.300d.txt
    with open('glove.6B.300d.txt','r',encoding="utf8") as f:
        for line in tqdm(f):
            values=line.split()
            word=values[0]
            vectors=np.asarray(values[1:],'float32')
            # vectors: 300 dimension
            embedding_dict[word]=vectors
    f.close()
    return embedding_dict


def glove_vectorisation(embedding_dict, corpus):
    MAX_LEN=50
    tokenizer_obj=Tokenizer()
    #The class allows to vectorize a text corpus, by turning each text into a sequence of integers (each integer being the index of a token in a dictionary)
    #{1: 'r', 2: 'day', 3: 'india', 4: 'offic', 5: 'collect', 6: 'said', 7: 'box', 8: 'crore', 9: 'year', 10: 'per', 11: 'new',..........}
    #10619 such tokens in the corpus  
    tokenizer_obj.fit_on_texts(corpus)
    
    sequences=tokenizer_obj.texts_to_sequences(corpus)
    #texts_to_sequences: Transforms each text in texts to a sequence of integers.
    #[24, 11, 119, 25, 43, 577, 449, 11, 110, 176, 1732] # list of integers for let's say first news' Synopsis
    word_index=tokenizer_obj.word_index
    #new dictionary initialized with the name=value pair in the keyword argument list. For example: dict(one=1, two=2)
    num_words=len(word_index)+1
    embedding_matrix=np.zeros((num_words,300))
    
    for word,i in tqdm(word_index.items()):
        if i > num_words:
            continue
        
        emb_vec=embedding_dict.get(word)
        if emb_vec is not None:
            embedding_matrix[i]=emb_vec
    return embedding_matrix



def tfidf_vectorizer(news_csv):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(news_csv['Synopsis'])
    return X , vectorizer
 
   
#The KMeans algorithm clusters data by trying to separate samples in n groups of equal variance, minimizing a criterion known as the 
#inertia or within-cluster sum-of-squares (see below). This algorithm requires the number of clusters to be specified.
def KmeansClustering(X):
    wcss=[]
    for i in tqdm(range(2,10)):
        model=KMeans(n_clusters=i,random_state=42)
        model.fit(X)
        wcss.append(model.inertia_)
        print(model.n_iter_)
    return (model , wcss)


def elbow_curve(wcss):   
    plt.figure(figsize=(10,10)) 
    plt.title("ELBOW METHOD")   
    plt.plot(range(2,10),wcss,label='ELBOW METHOD')
    plt.xlabel("Numbe of cluster")
    plt.ylabel("Wcss Value")
    plt.show()


def silhouette_curve(model,X):  
    # Instantiate the KElbowVisualizer with the number of clusters and the metric 
    visualizer = KElbowVisualizer(model, k=(2,10), metric='silhouette', timings=False)
    
    # Fit the data and visualize
    visualizer.fit(X)    
    visualizer.poof() 
 
news_csv= pd.read_csv("news_corpus_processed.csv",encoding="utf8")    

#glove
corpus = create_corpus(news_csv)
embedding_dict = pre_trainModel()
embedding_matrix = glove_vectorisation(embedding_dict, corpus)
model , wcss = KmeansClustering(embedding_matrix)
elbow_curve(wcss)
silhouette_curve(model , embedding_matrix)


#tfid
X , vectorizer= tfidf_vectorizer(news_csv)
model , wcss = KmeansClustering(X)
elbow_curve(wcss)
silhouette_curve(model,X)


true_k = 8

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :100]:
        print(' %s' % terms[ind],end='')
    print()
























