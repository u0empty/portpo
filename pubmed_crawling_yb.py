#!/usr/bin/env python
# coding: utf-8

# In[24]:


import pandas as pd
import re
import urllib
from time import sleep


# In[25]:


query = "periodontitis"


# In[26]:


base_url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
db = 'db=pubmed'


# In[27]:


search_eutil = 'esearch.fcgi?'
search_term = '&term=' + query
search_usehistory = '&usehistory=y'
search_rettype = '&rettype=json'


# In[28]:


search_url = base_url+search_eutil+db+search_term+search_usehistory+search_rettype
print("this is the esearch command:\n" + search_url + "\n")


# In[29]:


f = urllib.request.urlopen (search_url)


# In[30]:


search_data = f.read().decode('utf-8')
search_url = base_url+search_eutil+db+search_term+search_usehistory+search_rettype
print("this is the esearch command:\n" + search_url + "\n")


# In[37]:


f = urllib.request.urlopen (search_url)
search_data = f.read().decode('utf-8')


# In[32]:


total_abstract_count = int(re.findall("<Count>(\d+?)</Count>",search_data)[0])


# In[33]:


fetch_eutil = 'efetch.fcgi?'
retmax = 20
retstart = 0
fetch_retmode = "&retmode=text"
fetch_rettype = "&rettype=abstract"


# In[34]:


fetch_webenv = "&WebEnv=" + re.findall ("<WebEnv>(\S+)<\/WebEnv>", search_data)[0]
fetch_querykey = "&query_key=" + re.findall("<QueryKey>(\d+?)</QueryKey>",search_data)[0]


# In[38]:


print(search_data)


# In[41]:


total_abstract_count


# In[39]:


fetch_webenv


# In[47]:


fetch_querykey


# In[42]:


fetch_eutil = 'efetch.fcgi?'
retmax = 20
retstart = 0
fetch_retstart = "&retstart=" + str(retstart)
fetch_retmax = "&retmax=" + str(retmax)
fetch_retmode = "&retmode=text"
fetch_rettype = "&rettype=abstract"


# In[43]:


fetch_url = base_url+fetch_eutil+db+fetch_querykey+fetch_webenv+fetch_retstart+fetch_retmax+fetch_retmode+fetch_rettype
print(fetch_url)


# In[44]:


f = urllib.request.urlopen (fetch_url)


# In[45]:


fetch_data = f.read().decode('utf-8')


# In[49]:


fetch_data[:3000]


# In[50]:


abstracts = fetch_data.split("\n\n\n")
len(abstracts)


# In[55]:


abstracts[0]


# In[52]:


split_abstract = abstracts[0].split("\n\n")
split_abstract


# In[56]:


run = True
all_abstracts = list()
loop_counter = 1
retmax = 20
retstart = 0

while run: 
    print("this is efetch run number " + str(loop_counter))
    loop_counter += 1
    fetch_retstart = "&retstart=" + str(retstart) # 몇 번째 논문부터 시작?
    fetch_retmax = "&retmax=" + str(retmax) # 몇 번째 논문까지?
    # 요청 url 완성시키기
    fetch_url = base_url+fetch_eutil+db+fetch_querykey+fetch_webenv+fetch_retstart+fetch_retmax+fetch_retmode+fetch_rettype
    print(fetch_url)
    # 텍스트 형태로 논문 20개 가져오기
    f = urllib.request.urlopen (fetch_url)
    fetch_data = f.read().decode('utf-8')
    
    # 리스트 형태로 논문을 서로 나누기
    abstracts = fetch_data.split("\n\n\n")
    # append to the list all_abstracts
    all_abstracts = all_abstracts+abstracts
    print("a total of " + str(len(all_abstracts)) + " abstracts have been downloaded.\n")
    # wait 2 seconds so we don't get blocked
    sleep(2)
    # update retstart to download the next chunk of abstracts
    retstart = retstart + retmax
    if retstart > total_abstract_count:
        run = False


# In[57]:


len(all_abstracts)


# In[58]:


test = all_abstracts[10]
test = test.split('\n\n')

all_abstracts[10]


# In[65]:


print('\n',test)


# In[60]:


def split_list(x):
    x = x.split('\n\n')
    return x[:5]


# In[61]:


list_abstracts = list(map(split_list, all_abstracts))
list_abstracts


# In[66]:


for i, a in enumerate(list_abstracts):
    print(i, len(a))


# In[63]:


test_df = pd.DataFrame(list_abstracts, columns=['journal', 'title', 'author', 'author_info', 'abstract'])

test_df


# In[67]:


test_journal = test_df.journal.unique()[0]
test_journal


# In[68]:


test_journal = test_journal.split(". ")
test_journal


# In[69]:


journal = test_journal[1]
print(journal)

year = test_journal[2][:4]
print(year)


# In[70]:


def get_journal(x):
    x = x.split(". ")
    try:
        journal = x[1]
    except:
        journal = 'None'
    return journal

def get_year(x):
    x = x.split(". ")
    try:
        year = x[2][:4]
    except:
        year = 'None'
    return year


# In[71]:


test_df['journal_name'] = test_df['journal'].map(get_journal)
test_df['year'] = test_df['journal'].map(get_year)

test_df


# In[72]:


test_df = test_df.drop(['journal'], axis=1)
test_df.head()


# In[73]:


test_df = test_df[['journal_name', 'year', 'title', 'author', 'author_info', 'abstract']]
test_df.head()


# In[74]:


test_df.abstract[0]


# In[ ]:




