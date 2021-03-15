import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from math import modf

# Declare constants
words_per_min = 200

# Convert minutes to minutes and seconds
def process_time(time):
    seconds, minutes = modf(time)           # separates decimal and integer part
    seconds *= 60
    if minutes == 0:
        return 1
    return minutes if seconds < 30 else minutes + 1

# Return Average Reading time for the articles
def avg_time(article):
    article_length = len(article.split())      # Split om the basis of space character to get number of words in an article
    time = article_length / words_per_min
    return process_time(time)

# Analyse the time for reading the article
def analyse():
    time_count  = news_corpus['Avg_Time'].value_counts()
    print(time_count)
    plt.figure(figsize=(10,5))
    sns.barplot(time_count.index, time_count.values, alpha=0.8)
    plt.title('Time Spent')
    plt.ylabel('Frequency', fontsize=12)
    plt.xlabel('Time', fontsize=12)
    plt.show()

# Importing "article" dataset
news_corpus = pd.read_csv("dataset/combined_csv_files/news_corpus_cleaned.csv",encoding = 'latin1')
news_corpus['Avg_Time'] = news_corpus['News'].apply(avg_time)

analyse()
# Save the data back to news_corpus_cleaned.csv with "avg_time" column added
news_corpus.to_csv('dataset/combined_csv_files/news_corpus_cleaned.csv', index = False, encoding='utf')
print("File Updated Successfully!!!")