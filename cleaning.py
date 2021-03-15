import pandas as pd

months = {
    'january': '01', 'february': '02', 'march': '03',
    'april': '04', 'may': '05', 'june': '06',
    'july': '07', 'august': '08', 'september': '09', 
    'october': '10', 'november': '11', 'december': '12'
}

# 'month day, year' --> 'YYYY-MM-DAY'
# Eg: 'September 9, 2020' --> '2020-09-09'
def format_date(date):
    date = date.replace(',','')
    date = date.lower()                             # Eg: 'September 9 2020' --> 'september 9 2020'
    date = date.split()                             # Split on the basis of 'spaces' 
    month, day, year = date[0], date[1], date[2]
    month = months[date[0]]                         # Eg: 'september' --> '09'
    day = day if len(day) == 2 else '0' + day       # Single digit day to double digit Eg: '8' --> '08'
    return year + "-" + month + "-" + day

# 12-hour format --> 24-hour format
# Eg: '1:41:37 AM' --> '01:41:37'
def format_time(time):
    time = time.lower()                             # 'AM' --> 'am' / 'PM' --> 'pm' (bringing uniformity in rows)
    time = time if len(time) == 11 else '0' + time  # '1:41:37 AM' --> '01:41:37 AM'(bringing uniformity in rows)
    if time.endswith('am') and time[:2] == "12": 
        time = "00" + time[2:-2]
        
    elif time.endswith('am'): 
        time = time[:-2]

    elif time.endswith('pm') and time[:2] == "12": 
        time = time[:-2]

    else:
        time = str(int(time[:2]) + 12) + time[2:8]
    return time.strip()                             # Stripping the extra spaces on the right and left of time

if __name__ == "__main__":
    # Loading 'news_corpus.csv' to dataframe 'dataset' for the processing
    dataset = pd.read_csv("dataset/combined_csv_files/news_corpus.csv", encoding = 'latin1')

    # Changing column names
    dataset.rename(columns={'Author/Publisher': 'Publisher'}, inplace = True)
    dataset.rename(columns={'SourceLink': 'Source_Link'}, inplace = True)

    # Formatting Date and Time
    dataset['Date'] = dataset['Date'].apply(format_date)
    dataset['Time'] = dataset['Time'].apply(format_time)

    # Other pre-processing operation(s)
    dataset['Publisher'] = dataset['Publisher'].str.upper()

    # Sorting articles as per 'Date and Time'
    dataset = dataset.sort_values(by = ['Date','Time'], ascending = True)

    # Giving 'article_id' to each news as per the date and time of there publication
    article_id = [i+1 for i in range(len(dataset))]
    dataset.insert(0, 'Article_id', article_id)

    # Processed dataframe 'dataset' saved to a new CSV 'news_corpus_cleaned.csv'
    dataset.to_csv('dataset/combined_csv_files/news_corpus_cleaned.csv', index = False, encoding='utf')