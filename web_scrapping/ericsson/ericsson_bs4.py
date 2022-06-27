#!/usr/bin/env python
# coding: utf-8

# In[1]:


import bs4
from bs4 import BeautifulSoup
import requests
import colorama
from colorama import Fore
from datetime import datetime
import pandas as pd , numpy as np ,re

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


titles = []
hrefs = []
dates = []
thumbnails = []

for p in range(1,5):
    
        
        #getting the urls
        
        url =  f'https://www.ericsson.com/en/newsroom/latest-news?typeFilters=1%2C2%2C3%2C4&locs=68304%2C46951&userMarket=46951&pageNum={p}'
        
        soup = parse_webpage_bs(url)
        
        date_container = soup.findAll('span', {'class': 'date'})
        
        for d_container in date_container:
            date  = d_container.text
            dates.append(date)
            
        title_container = soup.findAll('h4', {'class': 'card-title'})
        
        for t_container in title_container:
            title  = t_container.text
            titles.append(title)
            href = 'https://www.ericsson.com'+ t_container.find('a')['href']
            hrefs.append(href)

        img_container = soup.findAll('div', {'class': 'lg-3 sm-4 xs-12 mb-0 mb-sm-3'})
        
        for i_container in img_container:            
            thumb  = 'https://www.ericsson.com'+ i_container.find('img')['data-src' ]           
            thumbnails.append(thumb)
            
        print(f"scrapping done for page {p}")


# In[4]:


articles  = []

for number,link in enumerate (hrefs):
    
        soup = parse_webpage_bs(link)

        art_containers = soup.findAll('div', {'id' :'primarycontent'})

        for art in art_containers:
            article = art.text
            articles.append(article)
        
        print(f"scrapping done for url {number}")


# In[5]:


#zippling the list so that it'll form the tuple
zipped = list(zip(dates,titles,articles,hrefs,thumbnails))
zipped[:3]


# In[6]:


import pandas as pd


#creating dataframe 
temp_df = pd.DataFrame(zipped,columns=['date','title','article','url','thumbnail'])
temp_df


# In[7]:


#to csv
temp_df.to_csv('amazon news.csv')

#to json
temp_df.to_json('amazon news.json')

