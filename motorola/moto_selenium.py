#!/usr/bin/env python
# coding: utf-8

# https://www.motorola.com/blog/en-us/all-post-page

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
#                           ,options=option
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




driver.maximize_window()

url = f'https://www.motorola.com/blog/en-us/all-post-page'

driver.get(url)

driver.find_element_by_xpath('''/html/body/div[3]/div/div/div/div[2]/div/div[1]''').click()

driver.refresh()

hrefs = []

range_count = 3

try:
    for x in range(range_count):
        time.sleep(3)
        driver.find_element_by_xpath('''/html/body/div[2]/div/div[1]/div/div/div[2]/div/div/div/div[4]/div/a[2]''').click()

        for y in range(11):
            
            links = driver.find_elements_by_xpath(f'''/html/body/div[2]/div/div[1]/div/div/div[2]/div/div/div/div[3]/div[{y}]/a''')
            for l in links:
                hrefs.append(l.get_attribute('href'))

        print(str(range_count-(x+1)) + " pages remaining..",end="\r")
except:
    pass


# In[5]:




articles  = []
dates = []
titles = []
thumbnails = []

try:
    for number,link in enumerate(hrefs):

        driver.get(link)
        time.sleep(1)
        driver.implicitly_wait(100)
        title = driver.find_element_by_xpath('''/html/body/div[2]/div/div[1]/div/div/div[2]/div/div/div[1]/div[3]/div[2]/div/h1''').text
        titles.append(title)
        article = driver.find_element_by_xpath('''/html/body/div[2]/div/div[1]/div/div/div[2]/div/div/div[2]''').text
        articles.append(article)
        date = driver.find_element_by_xpath('''/html/body/div[2]/div/div[1]/div/div/div[2]/div/div/div[1]/div[3]/div[4]/div/span[2]''').text
        dates.append(date)
        thumbnail = driver.find_element_by_xpath('''/html/body/div[2]/div/div[1]/div/div/div[2]/div/div/div[1]/div[1]/img''').get_attribute('src')
        thumbnails.append(thumbnail)
        print(str(len(hrefs)-(number+1)) + " url remaining..",end="\r")


    print()
    
except:
    pass


# In[6]:


#zippling the list so that it'll form the tuple
zipped = list(zip(dates,titles,articles,hrefs,thumbnails))
zipped[:3]


# In[7]:


#creating dataframe 
temp_df = pd.DataFrame(zipped,columns=['date','title','article','url','thumbnail'])
temp_df.head()


# In[8]:


#to csv
temp_df.to_csv('salesforce news.csv')

#to json
temp_df.to_json('salesforce news.json')

