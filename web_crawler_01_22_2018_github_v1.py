#Copyright 2018 UNIST under XAI Project supported by Ministry of Science and ICT, Korea

#Licensed under the Apache License, Version 2.0 (the "License"); 
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

#   https://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

# coding: utf-8

# In[1]:

import os
import sys
from bs4 import BeautifulSoup
import requests
from __future__ import print_function, unicode_literals
import pandas as pd
import numpy as np
import csv


# In[3]:

#get webpage
def get_web(url):
    r=requests.get(url)
    c=r.content
    decoded=BeautifulSoup(c, 'html.parser')
    return decoded


# In[5]:

#get Naver Finance web page
exchange_address='http://finance.naver.com/marketindex/?tabSel=exchange#tab_section'
content=get_web(exchange_address)


# In[6]:

#find currency exchange rate
current_exchange=[]
for table in content.findAll('div', {'class':'data'}):
    for body in table.findAll('span', {'class':'value'}):
        current_exchange.append(body.string)


# In[8]:

#get web page2
rate_address='http://www.global-rates.com/interest-rates/central-banks/central-banks.aspx'
content2=get_web(rate_address)


# In[9]:

#find base interest rate
base_rate=[]
for table in content2.findAll('tr'):
      for body in table.findAll('tr', {'class':'tabledata1'}):
            for number in body.findAll('td'):
                 base_rate.append(number.string)

base_rate2=[]
for table in content2.findAll('tr'):
      for body in table.findAll('tr', {'class':'tabledata2'}):
            for number in body.findAll('td'):
                    base_rate2.append(number.string) 
                    
usd=base_rate[2].replace('\xa0','')
eur=base_rate[32].replace('\xa0','')
krw=base_rate2[8].replace('\xa0','')
cny=base_rate2[20].replace('\xa0','')
jpy=base_rate2[44].replace('\xa0','')


# In[10]:

exchange_rate_total=[current_exchange[0], current_exchange[2], current_exchange[1], current_exchange[3],'-']
base_rate_total=[usd, eur, jpy, cny, krw]
total=[exchange_rate_total, base_rate_total]

array=np.array(total)
df=pd.DataFrame(array, columns=['미국','유럽','일본','중국', '한국'])


# In[11]:

df.rename(index={0:"환전 고시 환율", 1:"기준 금리"})

