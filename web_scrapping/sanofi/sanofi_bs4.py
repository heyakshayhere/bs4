#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
import sys,bs4,re,time,requests,pandas as pd
from bs4 import BeautifulSoup

import warnings
warnings.filterwarnings("ignore")

get_ipython().run_line_magic('autosave', '1')


# In[2]:


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


# In[3]:


titles,hrefs,dates = [],[],[]
start_year = 2022
end_year = 2022

for y in range(start_year,end_year+1):
    url = f"https://www.sanofi.com/en/media-room/press-releases/{y}#"
    soup = parse_webpage_bs(url)
    
    all_container = soup.findAll('div',{'class' :'osw-pagelist-element-col osw-pagelist-element-col-100'})

    for d in all_container:
        date = d.text
        dates.append(date[:10])

    for h in all_container:
        href = "https://www.sanofi.com" + h.find("a")['href']
        hrefs.append(href)

    for t in all_container:
        title = t.find("a")['title']
        titles.append(title)   


# In[4]:


articles = []

for number,link in enumerate(hrefs):
    soup = parse_webpage_bs(link)
    article_container = soup.findAll('div',{'class' :'osw-page-content-inside osw-bg-white'})
    for p in article_container:
        articles.append(p.text)
    
    print(str(len(hrefs)-(number+1)) + " url remaining..",end="\r")


# In[5]:


#zippling the list so that it'll form the tuple
zipped = list(zip(dates,titles,articles,hrefs))
#creating dataframe 
temp_df = pd.DataFrame(zipped,columns=['date','title','article','url'])
temp_df.head()


# In[6]:


#to csv
temp_df.to_csv('sanofi news.csv')

#to json
temp_df.to_json('sanofi news.json')

