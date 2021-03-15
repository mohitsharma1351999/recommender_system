import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go

# Returns number of missing values
def check_missing_values(corpus):
    return corpus.isna().sum()

# Returns number of articles, number of publishers and number of Categories
def basic_stats(corpus):
    return dataset.shape[0], dataset["Publisher"].nunique(), dataset["Category"].nunique()
    
# Plot number of articles for each category 
def category_distribution(corpus):
    fig = go.Figure([go.Bar(x=dataset["Category"].value_counts().index, y=dataset["Category"].value_counts().values)])
    fig['layout'].update(title={"text" : 'Distribution of articles category-wise','y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'}, xaxis_title="Category name",yaxis_title="Number of articles")
    fig.update_layout(width=800,height=700)
    fig.show()

# Plot number of articles written every month
def monthly_distribution(corpus):
    dataset['Date'] = pd.to_datetime(dataset['Date'])
    news_articles_per_month = dataset.resample('m',on = 'Date')['Title'].count()   
    fig = go.Figure([go.Bar(x=news_articles_per_month.index.strftime("%b"), y=news_articles_per_month)])
    fig['layout'].update(title={"text" : 'Distribution of articles month-wise','y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'}, xaxis_title="Month",yaxis_title="Number of articles")
    fig.update_layout(width=500,height=500)
    fig.show()

# Distribution of "length of Titles"
def title_length(corpus):
    fig = ff.create_distplot([dataset['Title'].str.len()], ["ht"],show_hist=False,show_rug=False)
    fig['layout'].update(title={'text':'PDF','y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'}, xaxis_title="Length of a headline",yaxis_title="probability")
    fig.update_layout(showlegend = False,width=500,height=500)
    fig.show()

if __name__ == "__main__":
    dataset = pd.read_csv("dataset/combined_csv_files/news_corpus_cleaned.csv", encoding = 'latin1')
    print(check_missing_values(dataset))

    print("*****************************************")
    articles, publishers, categories = basic_stats(dataset)
    print("Total number of articles : ", articles)
    print("Total number of authors : ", publishers)
    print("Total number of unqiue categories : ", categories)

    category_distribution(dataset)
    monthly_distribution(dataset)
    title_length(dataset)