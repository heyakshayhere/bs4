#!/usr/bin/env python
# coding: utf-8

# https://news.adobe.com/news/default.aspx

# In[1]:


import pandas as pd,requests,bs4
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")

get_ipython().run_line_magic('autosave', '1')


# In[2]:


titles,thumbnails,hrefs = [],[],[]

range_count = 2023

for x in range(2021,range_count):
    try:
        api = f"https://news.adobe.com/feed/PressRelease.svc/GetPressReleaseList?apiKey=BF185719B0464B3CB809D23926182246&LanguageId=1&bodyType=0&pressReleaseDateFilter=3&categoryId=1cb807d2-208f-4bc3-9133-6a9ad45ac3b0&pageSize=-1&pageNumber=0&tagList=&includeTags=true&year={x}&excludeSelection=1"
        req = requests.get(api)
        json = req.json()
        try:
            for i in range(100):
                data = json['GetPressReleaseListResult'][i]
                title = data["Headline"]
                titles.append(title)
                href = "https://news.adobe.com/" + data["LinkToDetailPage"]
                hrefs.append(href)
                thumbnail = data["ThumbnailPath"]
                thumbnails.append(thumbnail)
        except:
            pass
    except:
        pass
    print(str(range_count-(x+1)) + " pages remaining..",end="\r")


# In[3]:


def parse_webpage_bs(search_url):
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"}
    try:
        site_request = requests.get(search_url, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        print(e)
        site_request = None
    if site_request != None and site_request.status_code==200:
        site_soup = bs4.BeautifulSoup(site_request.content, "lxml")
    else:
        site_soup = None
    return site_soup


# In[4]:


dates,articles = [],[]
range_count = len(href)

for number,link in enumerate(hrefs[:range_count]):
    soup = parse_webpage_bs(link)

    date_containers = soup.findAll('div',{'class' :'module_date-time'})

    for d in date_containers:
        date = (d.text).replace("\n","")
        dates.append(date)
    
    art_containers = soup.findAll('div',{'class' :'module_body'})

    for art in art_containers:
        article = art.text
        articles.append(article)

    print(str(len(hrefs)-(number+1)) + " url remaining..",end="\r")


# In[5]:


#zippling the list so that it'll form the tuple
zipped = list(zip(dates,titles,articles,hrefs,thumbnails))
#creating dataframe 
temp_df = pd.DataFrame(zipped,columns=['date','title','article','url','thumbnail'])
temp_df.head()


# In[6]:


#to csv
temp_df.to_csv('adobe news.csv')

#to json
temp_df.to_json('adobe news.json')

