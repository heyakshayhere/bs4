#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


#for formatting use this reference 
#https://www.geeksforgeeks.org/python-strftime-function/#:~:text=The%20strftime()%20function%20is,and%20returns%20the%20string%20representation.&text=Returns%20%3A%20It%20returns%20the%20string,the%20date%20or%20time%20object.
# creating the list of dates 
list_of_dates = []

try:
    #taking input from user
#     start_date = input("Enter start date (in YYYY MM DD) : " )
#     end_date = input("Enter end date (in YYYY MM DD) : " )
    start_date = '2022 1 1'
    end_date = '2022 4 20'

    #adding up condition 
    if start_date > end_date :
        print(Fore.RED+ '\nstart date must come before end date')

    #appending to the list includes both dates
    else:
        for d in pd.date_range(start_date, end_date,inclusive="both"):
            list_of_dates.append(d.strftime("%B %#d, %Y"))

#dealing with error/s    
except ValueError:
    print(Fore.RED +"\nAdd the dates in correct format (in YYYY MM DD)")


# In[3]:


def unix_to_datetime(unix_value:int):
    a = datetime.utcfromtimestamp(1650513646)
    return a.strftime("%B %#d, %Y")


# In[4]:


#there are 127 pages in total


# In[5]:


titles = []
hrefs = []
dates = []

for p in range(1,10):
    
        #getting the urls
        url =  f'https://www.aboutamazon.com/news?p={p}'

        #parsing
        source = requests.get(url)
        soup = BeautifulSoup(source.content,'lxml')
        
        all_containers = soup.findAll('li', {'class': 'SearchResultsModuleResults-items-item'})
        
        for container in all_containers:
            title  = container.find('h2').text.strip()
            titles.append(title)
            href = container.find('a')['href']
            hrefs.append(href)
            published_date = container.find('bsp-timestamp')['data-timestamp']
            published_date = int(str(published_date)[:-3])
            published_date = unix_to_datetime(published_date)
            dates.append(published_date)
        
        print(f"scrapping done for page {p}")


# In[6]:


articles  = []
thumbnails = []

for number,link in enumerate (hrefs):
        #getting the urls
        url =  link

        #parsing
        source = requests.get(url)
        soup = BeautifulSoup(source.content,'lxml')
        
        all_containers = soup.findAll('div', {'class' :'ArticlePage-wrapper'})
        
        for container in all_containers:
            article = container.text
            articles.append(article)
            
        img_container = soup.findAll('img', {'class' :'Image'})
        
        for thumb in img_container[:1]:
            thumbnail = thumb['src']
            thumbnails.append(thumbnail)
        
        print(f"scrapping done for url {number}")


# In[7]:


#zippling the list so that it'll form the tuple
zipped = list(zip(dates,titles,articles,hrefs,thumbnails))
zipped[:3]


# In[8]:


import pandas as pd


#creating dataframe 
temp_df = pd.DataFrame(zipped,columns=['date','title','article','url','thumbnail'])
temp_df


# In[9]:


#to csv
temp_df.to_csv('amazon news.csv')

#to json
temp_df.to_json('amazon news.json')

