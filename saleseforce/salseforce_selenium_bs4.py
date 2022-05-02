#!/usr/bin/env python
# coding: utf-8

# https://www.salesforce.com/news/all-news/

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
import sys,bs4,re,time,requests,pandas as pd
from bs4 import BeautifulSoup

import warnings
warnings.filterwarnings("ignore")

get_ipython().run_line_magic('autosave', '1')


# In[2]:


#driver for operation
from webdriver_manager.chrome import ChromeDriverManager
option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(ChromeDriverManager().install()
                          ,options=option
                         )


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




url = f'https://www.salesforce.com/news/all-news/'

driver.get(url)

driver.refresh()

hrefs = []

range_count = 10

for x in range(range_count):
    driver.implicitly_wait(100)
    driver.find_element_by_xpath('''/html/body/main/div/div/div/div/div/span''').click()
    print(str(range_count-(x+1)) + " pages remaining..",end="\r")

links = driver.find_elements_by_xpath('''/html/body/main/div/div/div/div/a''')

for l in links:
    hrefs.append(l.get_attribute("href"))


# In[5]:




articles  = []
dates=[]
titles=[]
thumbnails=[]

for number,link in enumerate(hrefs):
    
    soup = parse_webpage_bs(link)

    art_containers = soup.findAll('section',{'class' :'the-content'})

    for art in art_containers:
        article = art.text
        articles.append(article)

    t_containers = soup.findAll('h1',{'class' :'hero__title'})

    for t in t_containers:
        title = t.text
        titles.append(title)

    d_containers = soup.findAll('p',{'class' :'byline__date'})

    for d in d_containers:
        date = d.text
        dates.append(date)
        
    thumb_containers = soup.findAll('figure',{'class' :'wp-block-image prevent-download'})

    for thumb in thumb_containers:
        thumbnail = thumb.find('img')['src']
        thumbnails.append(thumbnail)

    print(str(len(hrefs)-(number+1)) + " url remaining..",end="\r")

    
print()


# In[6]:


#zippling the list so that it'll form the tuple
zipped = list(zip(dates,titles,articles,hrefs,thumbnails))
zipped[:3]


# In[7]:


#creating dataframe 
temp_df = pd.DataFrame(zipped,columns=['date','title','article','url','thumbnail'])
temp_df


# In[8]:


#to csv
temp_df.to_csv('salesforce news.csv')

#to json
temp_df.to_json('salesforce news.json')

