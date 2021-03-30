#!/usr/bin/env python
# coding: utf-8

# ## 使用pandas读取"Crime Statistics"的数据

# In[1]:


import pandas as pds

data = pds.read_csv('./Oakland Crime Statistics 2011 to 2016/records-for-2011.csv') 
data.dropna(how='all', inplace=True)


# ## 数值属性的五数概括

# In[2]:


data[['Area Id', 'Priority']].describe()


# In[3]:


data.head(3)


# ## 标称属性的聚会频数

# In[4]:


data['Agency'].value_counts()


# In[5]:


data['Create Time'].value_counts()


# In[6]:


data['Location'].value_counts()


# In[7]:


data['Beat'].value_counts()


# In[8]:


data['Incident Type Id'].value_counts()


# In[9]:


data['Incident Type Description'].value_counts()


# In[10]:


data['Event Number'].value_counts()


# In[11]:


data['Closed Time'].value_counts()


# ## 数值属性Area Id的缺失值个数

# In[12]:


data['Area Id'].isnull().sum()


# ## 数值属性Priority的缺失值个数

# In[13]:


data['Priority'].isnull().sum()


# ## 数值属性Area Id的直方图和盒图

# In[14]:


data.hist(['Area Id'])


# In[15]:


data.boxplot(['Area Id'])


# ## 数值属性Priority的直方图和盒图

# In[16]:


data.hist(['Priority'])


# In[17]:


data.boxplot(['Priority'])


# In[18]:


data['Area Id'].value_counts()


# In[19]:


data['Priority'].value_counts()


# ## 剔除缺失值先后Area Id的直方图、盒图和五数概括对比

# In[20]:


dropped_data = data.dropna(subset=['Area Id'])
cmp_dropped_area = pds.DataFrame({'original': data['Area Id'], 'dropped': dropped_data['Area Id']})
cmp_dropped_area.hist()


# In[21]:


cmp_dropped_area.boxplot()


# In[22]:


cmp_dropped_area.describe()


# ## 以最高频率值填补缺失值，以及填补前后的直方图、盒图和五数概括对比

# In[23]:


most_freq = data['Area Id'].value_counts().index[0]
area_fillna_freq = data['Area Id'].fillna(most_freq)
cmp_fillna_freq_area = pds.DataFrame({'original': data['Area Id'], 'fillna': area_fillna_freq})
cmp_fillna_freq_area.hist()


# In[24]:


cmp_fillna_freq_area.boxplot()


# In[25]:


cmp_fillna_freq_area.describe()


# ## 由于Area Id不符合正态分布，无法使用皮尔逊相关系数通过属性的相关关系来填补缺失值

# In[26]:


import scipy.stats as ss
dropped = data.dropna(subset=['Area Id', 'Priority'])

ss.normaltest(dropped['Area Id'])


# In[27]:


dropped['Area Id'].corr(dropped['Priority'], method='pearson')


# ## 计算数据对象相似性的函数，为了减少计算量而只考虑缺失值与附近20个对象的相似性

# In[28]:


def sim(e1, e2):
    score = 0
    score += int(e1['Agency'] == e2['Agency'])
    score += int(e1['Create Time'] == e2['Create Time'])
    score += int(e1['Location'] == e2['Location'])
    score += abs(e1['Priority'] - e2['Priority'])
    score += int(e1['Beat'] == e2['Beat'])
    score += int(e1['Incident Type Id'] == e2['Incident Type Id'])
    score += int(e1['Incident Type Description'] == e2['Incident Type Description'])
    score += int(e1['Event Number'] == e2['Event Number'])
    score += int(e1['Closed Time'] == e2['Closed Time'])
    return score

def get_fill_value(e0, pos):
    head = pos - 10 if pos - 10 >= 0 else 0
    tail = pos + 10 if pos + 10 <= len(data) else len(data)
    scores = data.loc[range(head, tail)].apply(lambda e: sim(e0, e), axis=1)
    sorted_scores = pds.DataFrame({'score': scores}).sort_values(['score'], ascending=False)
    for i, pos in enumerate(sorted_scores.index.tolist()):
        if i == 0 or data['Area Id'].isnull().values[pos]:
            continue
        else:
            return data['Area Id'].loc[pos]


# ## 使用最相似的数据对象对应的值来填补缺失值

# In[29]:


most_sim = pds.DataFrame({'Area Id': data['Area Id']})
col_num = data['Area Id'][data['Area Id'].isnull().values==True].index
for i in col_num:
    most_sim['Area Id'].loc[i] = get_fill_value(data.loc[i], i)


# ## 填补后的直方图、盒图和五数概括对比

# In[30]:


cmp_fillna_sim_area = pds.DataFrame({'original': data['Area Id'], 'fillna': most_sim['Area Id']})
cmp_fillna_sim_area.hist()


# In[31]:


cmp_fillna_sim_area.boxplot()


# In[32]:


cmp_fillna_sim_area.describe()

