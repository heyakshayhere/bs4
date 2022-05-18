#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd,requests

import warnings
warnings.filterwarnings("ignore")


# In[2]:


def parse_webpage_api(search_url):
    try:
        req = requests.get(search_url)
        data = req.json()
        return data
    except:
        return []


# In[3]:


def remove_esc_chars(text):
    return text.replace("\n", " ").replace("\t", " ").replace("\r", " ")


# In[4]:


article_list = []

pagination = 0 
while True:
    url = f"https://www.foxconn.com/api/en-us/news?page={pagination}"
    data = parse_webpage_api(url)
    last_page = data['last_page']
    if data != None:
        elements = data['data']
        for element in elements:
            title = element['title'].strip()
            thumbnail = element['thumbnail'].strip()
            content = element['content'].strip()
            text = remove_esc_chars(content)
            published_date = element['published_date'].strip()
            link = ("https://www.foxconn.com/en-us/press-center/press-releases/latest-news/" + str(element ['id'])).strip()
            article = (published_date,title,text,link,thumbnail)
            article_list.append(article)
    print(str(last_page-(pagination+1)) + " pages remaining..",end="\r")
    
    pagination +=1
    if pagination >= last_page:
        break


# In[5]:


temp_df = pd.DataFrame(article_list,columns=['date','title','article','url','thumbnail'])
temp_df


# In[6]:


#to csv
temp_df.to_csv('foxconn news.csv')

#to json
temp_df.to_json('foxconn news.json')

