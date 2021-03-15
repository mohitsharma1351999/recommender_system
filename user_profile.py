import random
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from math import modf

# Convert minutes to minutes and seconds
def process_time(time):
    seconds, minutes = modf(time)
    seconds *= 0.60
    if seconds >= 0.60:
        return round(minutes + 1, 2)
    return round(minutes + seconds)

# Assign scores to the articles as per the time spent by different users
def assign_score(percent_read):
    if percent_read == 0:
        return 0
    elif percent_read > 0 and percent_read <= 20:
        return 1
    elif percent_read > 20 and percent_read <= 40:
        return 2
    elif percent_read > 40 and percent_read <= 60:
        return 3
    elif percent_read > 60 and percent_read <= 80:
        return 4
    else:
        return 5

# Retrieve the Average time for reading an arcticle from the "News Corpus" Dataset
def get_time(article):
    return news_corpus.loc[news_corpus['Article_id'] == article, 'Avg_Time'].item()

# Show the distribution of Data
def visualize_data(session_id, user_id):
    # Display Session Id's Generated
    sns.distplot(session_id, kde = False)
    plt.show()
    # Display User Id's generated
    plt.hist(user_id)
    plt.show()

def display_distribution():
    print("Score Distribution")
    print(user_data['score'].value_counts())

    print("Read Articles Distribution")
    print(user_data['articles_read'].value_counts())

    print("Session Distribution")
    print(user_data['session_id'].value_counts())

    print("User Distribution")
    print(user_data['user_id'].value_counts())

# Required entry for the "User Data set"
user_data_size = 10000

# Importing "article" dataset and count number of articles
news_corpus = pd.read_csv("dataset/combined_csv_files/news_corpus_cleaned.csv",encoding = 'latin1')
article_count = len(news_corpus) - 1  # Not to include headings

# User profile frame
user_data = pd.DataFrame()

# Temporary frame for storing intermediate data
tmp_df = pd.DataFrame()

# Generating the Session Id's which will be around 1452811 
session_id = np.random.poisson(lam = 1425811, size = user_data_size)
user_data['session_id'] = session_id

# Creating 50 users distributed among the whole dataset
user_id = np.random.randint(50, size = user_data_size) + 1 
user_data['user_id'] = user_id

"""
Generating the "articles" read by the users.
They are generated with the conditions:
1. Same users should not get the same articles
2. Articles should be repeated among different users
"""

articles = []
uniq_user_id = np.unique(user_id)
for x in uniq_user_id:                      # Generating articles for all users from 1 to n
    count_x = np.count_nonzero(user_id == x)
    article_read = random.sample(range(1, article_count + 1), count_x)
    articles.extend(article_read)
user_data.sort_values(by = 'user_id', inplace = True)
user_data['articles_read'] = articles


tmp_df['Avg_Time'] = user_data['articles_read'].apply(get_time)

# Compute time taken by user to read the article
user_data['read_time'] = np.random.uniform(low = 0, high = 1.2, size = user_data_size) * tmp_df['Avg_Time']
user_data['read_time'] = user_data['read_time'].apply(process_time)

# Assigning Score/Rating to each article that are read by the users
tmp_df['percent_read'] = user_data['read_time'] / tmp_df['Avg_Time'] * 100
user_data['score'] = tmp_df['percent_read'].apply(assign_score)

# Visualise and Analyse Data
# visualize_data(session_id, user_id)
display_distribution()

# Order as per Session id and Save data to "user_profile.csv"
user_data.sort_values(by = 'session_id', inplace = True)
user_data.to_csv('dataset/combined_csv_files/user_profile.csv', index = False, encoding='utf')
print("Dataset Created!!!")