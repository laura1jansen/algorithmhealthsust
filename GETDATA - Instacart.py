#!/usr/bin/env python
# coding: utf-8

# In[24]:


import pandas as pd
import numpy as np

## Read in the transaction data (select correct path for each of the files)
order_products_prior = pd.read_csv(r"....\order_products__prior.csv", sep = ',', skipinitialspace = True)
orders = pd.read_csv(r"....\orders.csv", sep = ',', skipinitialspace = True)
products = pd.read_csv(r"....\products.csv", sep = ',', skipinitialspace = True)
departments = pd.read_csv(r"....\departments.csv", sep = ',', skipinitialspace = True)
aisles = pd.read_csv(r"....\aisles.csv", sep = ',', skipinitialspace = True)


# In[25]:


orders_prior = pd.merge(order_products_prior, orders, left_on='order_id', right_on='order_id', how='left')
orders_products = pd.merge(orders_prior, products, left_on='product_id', right_on='product_id', how='left')
orders_departments = pd.merge(orders_products, departments, left_on='department_id', right_on='department_id', how='left')
all_orders = pd.merge(orders_departments, aisles, left_on='aisle_id', right_on='aisle_id', how='left')


# In[26]:


print(all_orders.head(5))


# In[27]:


import numpy as np
import pandas as pd

# ADD product quantity (how much of each product was bought, can differ each order)
product_quantity = np.random.choice([1, 2, 3, 4], size=len(all_orders), p=[0.5, 0.2, 0.2, 0.1])
all_orders['PRODUCT_QUANTITY'] = product_quantity

print(all_orders.head(40))


# In[28]:


## ADD ratings: same rating for product each time it is bought
# Create a mapping of unique products to random values
product_mapping = pd.Series(np.random.choice([1, 2, 3, 4, 5], size=all_orders['product_id'].nunique(), p=[0.2, 0.2, 0.2, 0.2, 0.2]), index=all_orders['product_id'].unique())

# Map the values to the original DataFrame
all_orders['ratings'] = all_orders['product_id'].map(product_mapping)

num_products = len(all_orders['ratings'].dropna())
print("Number of products in the RATINGS column: " + str(num_products))

# Number of unique products per each cell value in the RATINGS column
products_per_value = all_orders.groupby('ratings')['product_id'].nunique()
print("Number of unique products per cell value in the RATINGS column:")
print(products_per_value)


# In[29]:


## ADD NUTRISCORE per product: same score each time it is bought
# Create a mapping of unique products to random values
product_mapping = pd.Series(np.random.choice([0, 1, 2, 3, 4, 5], size=all_orders['product_id'].nunique(), p=[0.78, 0.08, 0.03, 0.03, 0.05, 0.03]), index=all_orders['product_id'].unique())

# Map the values to the original DataFrame
all_orders['NUTRISCORE'] = all_orders['product_id'].map(product_mapping)

num_products = len(all_orders['NUTRISCORE'].dropna())
print("Number of products in the NUTRISCORE column: " + str(num_products))

# Number of unique products per each cell value in the NUTRISCORE column
products_per_value = all_orders.groupby('NUTRISCORE')['product_id'].nunique()
print("Number of unique products per cell value in the NUTRISCORE column:")
print(products_per_value)


# In[30]:


## ADD ORGANIC per product: same score each time it is bought (50% 1, 50% 0)
# Create a mapping of unique products to random values
product_mapping = pd.Series(np.random.choice([0, 1], size=all_orders['product_id'].nunique(), p=[0.50, 0.50]), index=all_orders['product_id'].unique())

# Map the values to the original DataFrame
all_orders['ORGANIC50'] = all_orders['product_id'].map(product_mapping)

num_products = len(all_orders['ORGANIC50'].dropna())
print("Number of products in the ORGANIC column: " + str(num_products))

# Number of unique products per each cell value in the ORGANIC50 column
products_per_value = all_orders.groupby('ORGANIC50')['product_id'].nunique()
print("Number of unique products per cell value in the ORGANIC50 column:")
print(products_per_value)


# In[31]:


## change names of variables into same as Dutch retailer data 
all_orders.rename(columns={'order_id': 'ORDER_ID'}, inplace=True)
all_orders.rename(columns={'product_id': 'PRODUCT_ID'}, inplace=True)
all_orders.rename(columns={'user_id': 'CUSTOMER_ID'}, inplace=True)
all_orders.rename(columns={'eval_set': 'EVAL_SET'}, inplace=True)
all_orders.rename(columns={'product_name': 'OMSCHRIJVING'}, inplace=True)
all_orders.rename(columns={'department': 'HOOFDCATEGORIE'}, inplace=True)
all_orders.rename(columns={'aisle': 'SUBCATEGORIE'}, inplace=True)


# In[33]:


print(all_orders.shape)


# In[34]:


#select 25% of the data
all_orders_25 = all_orders.head(int(len(all_orders) * 0.25))


# In[36]:


## 1. remove ITEMS that are not bought enough 

product_counts = all_orders_25['PRODUCT_ID'].value_counts() 

products_to_keep = product_counts[product_counts >= 3].index

df10 = pd.DataFrame(products_to_keep, columns=['PRODUCT_ID']) #create second dataframe with the ITEMS that should be kept
print(df10)
df11 = all_orders_25.merge(df10, on=['PRODUCT_ID'], how='left', indicator=True).query('_merge == "both"').drop(columns='_merge')
print(df11.shape)


# In[37]:


print(str(len(df11['CUSTOMER_ID'].unique())) +' unique customers')
min_basket_per_user = df11.groupby('CUSTOMER_ID')['ORDER_ID'].nunique().min()
print("Min basket per user: " + str(min_basket_per_user))


# In[38]:


## 2. KEEP ONLY BASKETS WITH >= 3 ITEMS 

basket_sizes = df11['ORDER_ID'].value_counts()

orders_to_keep = basket_sizes[basket_sizes >= 3].index    

df12 = pd.DataFrame(orders_to_keep, columns=['ORDER_ID']) #create second dataframe with the ORDER_IDs that should be kept 

df13 = df11.merge(df12, on=['ORDER_ID'], how='left', indicator=True).query('_merge == "both"').drop(columns='_merge')
print(df13.shape)


# In[39]:


print(str(len(df13['CUSTOMER_ID'].unique())) +' unique customers')
min_basket_per_user = df13.groupby('CUSTOMER_ID')['ORDER_ID'].nunique().min()
print("Min basket per user: " + str(min_basket_per_user))


# In[40]:


## 3. remove USERS with <3 orders(baskets)

order_counts_peruser = df13.groupby('CUSTOMER_ID')['ORDER_ID'].nunique()

users_to_keep = order_counts_peruser[order_counts_peruser >=3].index
print(users_to_keep)
df14 = pd.DataFrame(users_to_keep, columns=['CUSTOMER_ID']) #create second dataframe with the USERS that should be kept
print(df10)
df15 = df13.merge(df14, on=['CUSTOMER_ID'], how='left', indicator=True).query('_merge == "both"')
print(df11.shape)


# In[41]:


# Check if preprocessing went correctly
average_basket_size = df15.groupby('ORDER_ID')['PRODUCT_ID'].count().mean()
min_basket_size = df15.groupby('ORDER_ID')['PRODUCT_ID'].count().min()
max_basket_size = df15.groupby('ORDER_ID')['PRODUCT_ID'].count().max()
print("Average basket size: " + str(average_basket_size))
print("Min basket size: " + str(min_basket_size))
print("Max basket size: " + str(max_basket_size))

average_basket_per_user = df15.groupby('CUSTOMER_ID')['ORDER_ID'].nunique().mean()
min_basket_per_user = df15.groupby('CUSTOMER_ID')['ORDER_ID'].nunique().min()
max_basket_per_user = df15.groupby('CUSTOMER_ID')['ORDER_ID'].nunique().max()
print("Average basket per user: " + str(average_basket_per_user))
print("Min basket per user: " + str(min_basket_per_user))
print("Max basket per user: " + str(max_basket_per_user))


# In[43]:


print(df15.shape)


# In[45]:


## convert all cells + headers to upper for easy analysis later
df15 = df15.applymap(lambda x: x.upper() if isinstance(x, str) else x)    
df15.columns = map(str.upper, df15.columns)


# In[47]:


## save file as CSV
df15.to_csv("......csv", index=False, na_rep='NaN')  

