#!/usr/bin/env python
# coding: utf-8

# In[1]:


## Ignore  the warnings
import warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')
import time

## data visualisation and manipulation
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns


# In[2]:


## Load the merged data (see GETDATA notebook)
df2=pd.read_csv(r"NAME OF PATH", sep = ',', skipinitialspace = True)  # select your merged file here


# In[3]:


df2.head


# In[4]:


## Total number of unique consumers / orders / products / categories 

print("instacart")
print(str(len(df2['CUSTOMER_ID'].unique())) +' customers')
print(str(len(df2['ORDER_ID'].unique())) +' orders')
print(str(len(df2['PRODUCT_ID'].unique())) +' products')
print(str(len(df2['HOOFDCATEGORIE'].unique())) +' main categories')


average_basket_size = df2.groupby('ORDER_ID')['PRODUCT_ID'].count().mean()  #calculate also non-unique products in order
min_basket_size = df2.groupby('ORDER_ID')['PRODUCT_ID'].count().min()
max_basket_size = df2.groupby('ORDER_ID')['PRODUCT_ID'].count().max()
print("Average basket size: " + str(average_basket_size))
print("Min basket size: " + str(min_basket_size))
print("Max basket size: " + str(max_basket_size))

average_basket_per_user = df2.groupby('CUSTOMER_ID')['ORDER_ID'].nunique().mean()
min_basket_per_user = df2.groupby('CUSTOMER_ID')['ORDER_ID'].nunique().min()
max_basket_per_user = df2.groupby('CUSTOMER_ID')['ORDER_ID'].nunique().max()
print("Average basket per user: " + str(average_basket_per_user))
print("Min basket per user: " + str(min_basket_per_user))
print("Max basket per user: " + str(max_basket_per_user))


# In[5]:


# Number of products for the NUTRISCORE column
num_products = len(df2['NUTRISCORE'].dropna())
print("Number of products in the NUTRISCORE column: " + str(num_products))

# Number of unique products per each cell value in the NUTRISCORE column
products_per_value = df2.groupby('NUTRISCORE')['PRODUCT_ID'].nunique()
print("Number of unique products per cell value in the NUTRISCORE column:")
print(products_per_value)


# In[6]:


# Number of products for the ORGANIC column
num_products = len(df2['ORGANIC50'].dropna())
print("Number of products in the ORGANIC column: " + str(num_products))

# Number of unique products per each cell value in the ORGANIC column
products_per_value = df2.groupby('ORGANIC50')['PRODUCT_ID'].nunique()
print("Number of unique products per cell value in the ORGANIC column:")
print(products_per_value)


# In[7]:


## Barplot
x = sns.barplot(data = df2.groupby('HOOFDCATEGORIE')['ORDER_ID'].sum().sort_values(ascending = False).reset_index()[0:10], x = 'HOOFDCATEGORIE', y = 'ORDER_ID')
x.set_xticklabels(x.get_xticklabels(), rotation = 90)
x.set(xlabel = 'Category', ylabel = 'Products Ordered')


# In[8]:


## most popular items in terms of products ordered
x = sns.barplot(data = df2.groupby('OMSCHRIJVING')['ORDER_ID'].sum().sort_values(ascending = False).reset_index()[0:10], x = 'OMSCHRIJVING', y = 'ORDER_ID')
x.set_xticklabels(x.get_xticklabels(), rotation = 90)
x.set(xlabel = 'Product Name', ylabel = 'Order')


# In[9]:


## create barchart showing share instead of units for top products
product_share = df2.groupby('OMSCHRIJVING')['ORDER_ID'].sum().reset_index()
product_share['product_share'] = product_share['ORDER_ID']
product_share['product_share'] = product_share['product_share'].apply(lambda x: x / product_share['ORDER_ID'].sum())

x = sns.barplot(data = product_share.sort_values(by = 'product_share',ascending = False)[0:30], x = 'OMSCHRIJVING', y = 'product_share')
x.set_xticklabels(x.get_xticklabels(), rotation = 90)
x.set(xlabel = 'Product Name', ylabel = 'Unit Share')


# In[10]:


pd.set_option('display.min_rows',10000)
df2.groupby('OMSCHRIJVING')['ORDER_ID'].sum().sort_values(ascending = False)[0:100]


# In[11]:


df2.head

