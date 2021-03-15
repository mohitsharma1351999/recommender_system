import pandas as pd
dataset = pd.read_csv("news_corpus_processed.csv")
user_dataset = pd.read_csv("user_profile.csv")

latest_entertainment=(dataset.loc[dataset['Category'] == 'Entertainment']).tail()
latest_Lifestyle = (dataset.loc[dataset['Category'] == 'Lifestyle']).tail()
latest_Technology= (dataset.loc[dataset['Category'] == 'Technology']).tail()
latest_World= (dataset.loc[dataset['Category'] == 'World']).tail()
latest_Politics = (dataset.loc[dataset['Category'] == 'Politics']).tail()
latest_Sports=(dataset.loc[dataset['Category'] == 'Sports']).tail()
latest_Business= (dataset.loc[dataset['Category'] == 'Business']).tail()
latest_education = (dataset.loc[dataset['Category'] =='Education']).tail()

def latest_avgScore_news(latest_news , user_dataset):
    articles= list(latest_news['Article_id'])
    average_score = []
    for i in articles:
        user_news = user_dataset.loc[user_dataset['articles_read']==i]
        if user_news.empty:
            average_score.append(0)
        else :
            a = user_news['score'].mean()
            average_score.append(a) 
    print(average_score)
    Score = pd.DataFrame({'Article_id':articles,'Average Score':average_score})
    latest_news=(pd.merge(latest_news,Score ,on= 'Article_id' )).sort_values(by='Average Score')
    return latest_news

most_trending_entertainment = (latest_avgScore_news(latest_entertainment , user_dataset)).iloc[3:]
most_trending_Lifestyle = (latest_avgScore_news(latest_Lifestyle , user_dataset)).iloc[3:]
most_trending_Technology = (latest_avgScore_news(latest_Technology , user_dataset)).iloc[3:]
most_trending_World = (latest_avgScore_news(latest_World , user_dataset)).iloc[3:]
most_trending_Politics = (latest_avgScore_news(latest_entertainment , user_dataset)).iloc[3:]
most_trending_Sports = (latest_avgScore_news(latest_Sports , user_dataset)).iloc[3:]
most_trending_Business = (latest_avgScore_news(latest_Business , user_dataset)).iloc[3:]
most_trending_education = (latest_avgScore_news(latest_education , user_dataset)).iloc[3:]


final_recommend = (pd.concat([most_trending_entertainment, most_trending_Lifestyle,
                             most_trending_Technology, most_trending_World,
                             most_trending_Politics, most_trending_Sports,
                             most_trending_Business, most_trending_education]).sort_values(by='Average Score', ascending=False)).iloc[:10]






