from bs4 import BeautifulSoup
import requests as req
import csv
import pandas as pd

count = 0
f = csv.writer(open('data.csv', 'a',newline=''))

f.writerow([
    'Category','Sub_Category','Language',
    'Date','Time','Title','Synopsis','News',
    'Author/Publisher', 'Source Link'])

error_log_df = pd.DataFrame(columns = [
    'Url', 
    'Error'
])

categories = {
    'lifestyle':[
        'life-style' , 'health','food-wine','fashion',
        'books','relationships','destination-of-the-week',
        'fitness','art-and-culture','workplace'
        ], 
    'technology':[
        'gadgets', 'laptops',
         'mobile-tabs','science','techook'
        ]
    }

media_url = "https://indianexpress.com"

for category in categories:
    for sub_category in categories[category]:
        for page in range(1,8):
            # Getting to the list of news for each category on each of four pages (published recently)
            url = media_url + "/section/" + category + "/" + sub_category + "/" + "page/" + str(page) + "/"
            news_sheet = req.get(url)
            news_sheet_soup = BeautifulSoup(news_sheet.text, "html.parser")
            news_head_list = news_sheet_soup.findAll('h2', attrs={'class':'title'}) 
            for news_head in news_head_list:
                try:
                    news_url = news_head.find('a')['href']
                    print(news_url)
                    news = req.get(news_url)
                    soup = BeautifulSoup(news.text, 'html.parser')
    
    
                    title = soup.title.text
                    title=title[:title.index("|")]
                    
                    cat=[]
                    for l in soup.find_all("ol" , class_="m-breadcrumb"):
                        for link in l.find_all("a"):
                            c=link.text
                            if c !="Home":
                                cat.append(link.text)
                    for synopsis in soup.find_all('h2', class_='synopsis'):
                        synopsis_text = synopsis.text
                         
                    for d in soup.find_all("div" , id="storycenterbyline"):
                        for dt in d.find_all("span"):
                            date_time = dt.text.replace('Updated:', '')
                            date_time = date_time.strip()
                            date = date_time[: date_time.index("2020")+4]
                            time= date_time[date_time.index("2020")+5:]
                        for publisher in d.find_all("a"):
                            publisher_name = publisher.text
                            
                    news=''      
                    for n in soup.find_all("p", class_=''):  
                        news +=n.text
                    news=news.encode('ascii', 'ignore')
                    
                    
                    f.writerow([cat[0],cat[1],'English',date,time,title,synopsis_text,news,publisher_name,news_url])
                    
                    count+=1
                except Exception as e:
                    count += 1
                    print(count, "ERROR @ ", news_url) 
                    # Pushing the data to the DataFrame
                    error_log_df = error_log_df.append({
                        'Url' : news_url, 
                        'Error' : e},ignore_index = True)
