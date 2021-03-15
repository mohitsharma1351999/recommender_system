import requests
import html5lib
from bs4 import BeautifulSoup
import pandas as pd

# Category of News Required by me
categories = {
    'sports':[
        'badminton', 'cricket', 'football', 
        'fifa', 'hockey', 'motor-sport', 'tennis', 
        'wwe-wrestling'
        ], 
    'business':[
        'aviation', 'banking-and-finance',
        'companies', 'economy', 'market'
        ]
    }

# DataFrame to hold the News Data
news_corpus_df = pd.DataFrame(columns = [
    'Category',
    'Sub_Category',
    'Language',
    'Date',
    'Time',
    'Title',
    'Synopsis',
    'News',
    'Author/Publisher', 
    'Source Link'
])

# DataFrame to store the errors
error_log_df = pd.DataFrame(columns = [
    'Url', 
    'Error'
])

if __name__ == "__main__":
    # Url to Indian Express from where the news is to be gathered
    media_url = "https://indianexpress.com"

    for category in categories:
        for sub_category in categories[category]:
            for page in range(1,5):
                # Getting to the list of news for each category on each of four pages (published recently)
                news_sheet_url = media_url + "/section/" + category + "/" + sub_category + "/" + "page/" + str(page) + "/"
                news_sheet = requests.get(news_sheet_url)
                news_sheet_soup = BeautifulSoup(news_sheet.content,'html5lib')
                
                # Fetching news url for every article on a page from titles/headings for the news and reaching to that article/news
                news_head_list = news_sheet_soup.findAll('h2', attrs={'class':'title'}) 
                print(news_head_list)
                for news_head in news_head_list:
                    try:
                        news_url = news_head.find('a')['href']
                        news = requests.get(news_url)
                        news_soup = BeautifulSoup(news.content, 'html5lib')

                        # We reach here to the required article(news) thus collecting the required Information
                        # Fetching the title and description of the article/report/news
                        title = news_soup.find('h1',attrs={'class':'native_story_title'}).get_text()
                        synopsis = news_soup.find('h2', attrs={'class':'synopsis'}).get_text()

                        # Fetching the supporting details like author/publisher , date and time of publish
                        publishing_details = news_soup.find('div', attrs={'class':'editor'})
                        publisher = publishing_details.find('a').get_text()
                        date_time = publishing_details.find('span').get_text()
                        
                        # Processing and separating date and time
                        date_time = date_time.replace('Updated:', '')
                        date_time = date_time.strip()
                        date_time = date_time.split(",")
                        date = date_time[0] + ", " +  date_time[1].strip()[:4]
                        time = (date_time[1].strip()[5:]).strip()
                        
                        # Fetching the content of the news/article 
                        report = ""
                        report_paras = news_soup.findAll('p')
                        for para in range(len(report_paras)):
                            report += report_paras[para].get_text()
                        
                        # Pushing the data to the DataFrame
                        news_corpus_df = news_corpus_df.append({
                            'Category' : category.capitalize(),
                            'Sub_Category' : sub_category.capitalize(),
                            'Language' : 'English',
                            'Date' : date,
                            'Time' : time,
                            'Title' : title,
                            'Synopsis' : synopsis, 
                            'News' : report,
                            'Author/Publisher' : publisher.capitalize(), 
                            'Source Link' : news_url
                            },
                            ignore_index = True)
                    
                    except Exception as e:
                        print("ERROR @ ", news_url)
                        
                        # Pushing the data to the DataFrame
                        error_log_df = error_log_df.append({
                            'Url' : news_url, 
                            'Error' : e
                        },
                        ignore_index = True)
                        


        # Storing the DataFrame to a .csv file
        news_corpus_df.to_csv('dataset/separate_csv_files/' + category + '.csv', index = False, encoding='utf')

    # Storing the unscrapped data to csv
    error_log_df.to_csv('dataset/error.csv', index = False, encoding='utf')

