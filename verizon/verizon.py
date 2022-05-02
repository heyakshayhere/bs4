#!/usr/bin/env python
# coding: utf-8

# https://www.verizon.com/about/news/news-releases

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
import sys,bs4,re,time,requests,pandas as pd
from bs4 import BeautifulSoup

import warnings
warnings.filterwarnings("ignore")

get_ipython().run_line_magic('autosave', '1')


# In[ ]:


#driver for operation
from webdriver_manager.chrome import ChromeDriverManager
option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(ChromeDriverManager().install()
#                           ,options=option
                         )


# In[ ]:


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


# In[ ]:


url = f'https://www.verizon.com/about/news/news-releases'

driver.maximize_window()

driver.get(url)

hrefs = []

range_count = 3

for x in range(range_count):
    driver.implicitly_wait(100)
    driver.find_element_by_class_name('''nav-right_arrow ''').click()                                  
    for y in range(1,11):
        link = driver.find_element_by_xpath(f'''/html/body/div[2]/main/div/div/div[2]/div[2]/div/div/div/div/div/div[2]/div[2]/div[{y}]/div[3]/h2/a''').get_attribute("href")
        hrefs.append(link)                               
    print(str(range_count-(x+1)) + " pages remaining..",end="\r")


# In[ ]:


articles = []
dates = []
titles = []
thumbnails = []

for number,link in enumerate(hrefs):
    
    soup = parse_webpage_bs(link)

    t_containers = soup.findAll('div',{'class' :'news-fp-heading'})
    
    for t in t_containers:
        title = t.text
        titles.append(title)
    
    d_containers = soup.findAll('div',{'class' :'news-fp-date'})
    
    for d in d_containers:
        date = d.find('span').text
        dates.append(date)
        
    thumb_containers = soup.findAll('div',{'class' :'news-fp-image'})
    
    if len(thumb_containers) != 0:
        for thumb in thumb_containers:
            thumbnail = "https://www.verizon.com" + thumb.find('img')['src']
            thumbnails.append(thumbnail)
    else:
        thumbnails.append("")

    art_containers = soup.findAll('div',{'class' :'card'})
    
    for art in art_containers:
        article = art.text
        articles.append(article)
        
    print(str(len(hrefs)-(number+1)) + " url remaining..",end="\r")

    
print()


# In[ ]:


#zippling the list so that it'll form the tuple
zipped = list(zip(dates,titles,articles,hrefs,thumbnails))
zipped[:3]


# In[ ]:


#creating dataframe 
temp_df = pd.DataFrame(zipped,columns=['date','title','article','url','thumbnail'])
temp_df.head()


# In[ ]:


#to csv
temp_df.to_csv('salesforce news.csv')

#to json
temp_df.to_json('salesforce news.json')

