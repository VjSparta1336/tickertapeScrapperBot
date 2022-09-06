#!/usr/bin/env python
# coding: utf-8

# In[1]:


import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from lxml import html
from lxml import html
import xmltodict
import pandas as pd
import numpy as np
import os
from tqdm import tqdm


# In[2]:


stocks_sitemap = "https://www.tickertape.in/sitemaps/stocks/sitemap.xml"


# In[3]:


options = webdriver.ChromeOptions() 
options.add_argument("user-data-dir=""C:\\Users\\vatsal\\Hez\\Actual work\\Untitled Folder\\bse_chitthe_web_driver") #Path to your chrome profile
options.add_argument("--start-maximized")
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(executable_path= "chromedriver.exe", options=options)

driver.get(stocks_sitemap)


# In[4]:


sitemap=xmltodict.parse(driver.page_source)


# In[5]:


urls = []
for _ in sitemap['html']['body']['div'][0]['urlset']['url']:
    urls.append(_["loc"])


# In[6]:


driver.quit()


# In[5]:


def key_metrics(url,scode):
    driver.get(url)
    ratio_title = driver.find_elements(by=By.CLASS_NAME, value="key-ratio-title")
    ratio_value = driver.find_elements(by=By.CLASS_NAME, value="value")
    r_title = []
    for x in ratio_title:
        r_title.append(x.text)
    temp = []
    for x in ratio_value:
        temp.append(x.text)
    r_value = []
    for x in range(3,9):
        r_value.append(float(temp[x].replace("%", "").replace("—", "0")))
    key_metrics = dict(zip(r_title, r_value))
    os.system(f"mkdir -p tickertape\\{scode}")
    pd.to_pickle(key_metrics, f"./{scode}/key_metrics.pkl")
    


# In[6]:


def sheets(url,scode):
    finance = f"{url}/financials"
    driver.get(finance)
    dwnld_btn = driver.find_elements(by=By.CLASS_NAME, value="icon-download-data")
    balance_sheet=driver.find_elements(by=By.CLASS_NAME, value="segment-container")
    balance_sheet[1].click()
    dwnld_btn[0].click()
    balance_sheet[0].click()
    selector=driver.find_elements(by=By.CLASS_NAME, value="suggestion-toggle-btn")
    selector[0].click()
    qtrly=driver.find_elements(by=By.CLASS_NAME, value="segment-container")
    qtrly[3].click()
    dwnld_btn[0].click()
    balance_sheet[2].click()
    dwnld_btn[0].click()
    hold = f"{url}/holdings"
    driver.get(hold)
    dwnld_btn = driver.find_elements(by=By.CLASS_NAME, value="icon-download-data")
    dwnld_btn[1].click()


# In[4]:


os.system(f"mkdir -p tickertape")


# In[ ]:


for url in tqdm(urls):
    scode = url.split("-")[-1]
    options = webdriver.ChromeOptions() 
    options.add_argument("user-data-dir=""C:\\Users\\vatsal\\Hez\\Actual work\\Untitled Folder\\bse_chitthe_web_driver") #Path to your chrome profile
    options.add_argument("--start-maximized")
    options.add_argument('--disable-blink-features=AutomationControlled')
    prefs = {"download.default_directory" : f"C:\\Users\\vatsal\\Hez\\Actual work\\Untitled Folder\\tickertape\\{scode}"}
    options.add_experimental_option("prefs",prefs);
    driver = webdriver.Chrome(executable_path= "chromedriver.exe", options=options)
    key_metrics(url,scode)
    sheets(url,scode)
    driver.quit()


# In[2]:


os.system(f"mkdir -p hello")


# In[3]:


os.system(f"mkdir -p hello\\hi")


# In[ ]:




