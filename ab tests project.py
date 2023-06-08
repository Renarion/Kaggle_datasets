#!/usr/bin/env python
# coding: utf-8

# # We've got result of two campaigns:
#  - Control
#  - Test
# 
# # Below you can see all the features in the datasets: 
# 
# - Campaign Name: The name of the campaign (Groups)
# - Date: Date of the record (Date)
# - Spend: Amount spent on the campaign in dollars (Revenue)
# - of Impressions: Number of impressions the ad crossed through the campaign (Impressions)
# - Reach: The number of unique impressions received in the ad (Uniq_users)
# - of Website Clicks: Number of website clicks received through the ads (Clicks)
# - of Searches: Number of users who performed searches on the website (Searches)
# - of View Content: Number of users who viewed content and products on the website (Views)
# - of Add to Cart: Number of users who added products to the cart (a2c)
# - of Purchase: Number of purchases (Orders)

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import datetime
import seaborn as sns
import numpy as np
from datetime import datetime, date, timedelta
pio.templates.default = "plotly_dark"


# In[2]:


control_data = pd.read_csv('control_group.csv', sep=';')
test_data = pd.read_csv('test_group.csv', sep=';')


# In[3]:


print(control_data.head())
print(test_data.head())


# We have see that columns have mistakes at names.

# In[4]:


test_data.columns = ['Campaign name', 'Date', 'Amount spent', 'Number of impressions', 'Number of unique impressions', 'Number of website clicks', 'Searches', 'Views', 'Add to cart', 'Number of purchases']
control_data.columns = ['Campaign name', 'Date', 'Amount spent', 'Number of impressions', 'Number of unique impressions', 'Number of website clicks', 'Searches', 'Views', 'Add to cart', 'Number of purchases']


# In[5]:


print(test_data.isnull().sum())
print(control_data.isnull().sum())


# Method isnull() helps to check data on NULLs values and method sum() in the end helps us to sum this for useful format
# 
# The dataset of the control campaign has missing values in a row. Let’s fill in these missing values by the mean value of each column:

# In[7]:


control_data["Number of impressions"].fillna(value=control_data["Number of impressions"].mean(), 
                                             inplace=True)
control_data["Number of unique impressions"].fillna(value=control_data["Number of unique impressions"].mean(), 
                                             inplace=True)
control_data["Number of website clicks"].fillna(value=control_data["Number of website clicks"].mean(), 
                                             inplace=True)
control_data["Searches"].fillna(value=control_data["Searches"].mean(), 
                                             inplace=True)
control_data["Views"].fillna(value=control_data["Views"].mean(), 
                                             inplace=True)
control_data["Add to cart"].fillna(value=control_data["Add to cart"].mean(), 
                                             inplace=True)
control_data['Number of purchases'].fillna(value=control_data['Number of purchases'].mean(),
                                             inplace=True)


# Now I will create a new dataset by merging both datasets:

# In[34]:


ab_data = test_data.merge(control_data, how='outer').sort_values(by='Date')

ab_data = ab_data.reset_index(drop=True)
print(ab_data['Campaign name'].value_counts())
ab_data.head(10)


# # See all data on dependencies (Correlations) by campaign name

# In[102]:


sns.pairplot(ab_data, hue = 'Campaign name')


# # Check data for possible emissions

# In[101]:


#a2c
a2c = px.box(
        ab_data,
        x='Add to cart',
        color='Campaign name'
)

#views
views = px.box(
        ab_data,
        x='Views',
        color='Campaign name'
)

#searches
searches = px.box(
        ab_data,
        x='Searches',
        color='Campaign name'
)

#amount_spent
amount_spent = px.box(
        ab_data,
        x='Amount spent',
        color='Campaign name'
)


a2c.show()
views.show()
searches.show()
amount_spent.show()


# The dataset has 30 samples for each campaign. Now let’s start with A/B testing to find the best marketing strategy.

# In[86]:


px.scatter(ab_data,
              x='Number of impressions',
              y='Amount spent',
              size = 'Amount spent',
              color='Campaign name',
              trendline='ols'
          )


# In[33]:


#searches
searches_pie = go.Figure(data=[go.Pie(labels=["Total Searches from Control Campaign","Total Searches from Test Campaign"], 
                       values=[ab_data[ab_data['Campaign name']=='Test Campaign']['Searches'].sum(), 
                               ab_data[ab_data['Campaign name']=='Control Campaign']['Searches'].sum()],
                      )])
colors = ['gold', 'orange']
searches_pie.update_layout(title_text='Control Vs Test: Searches')
searches_pie.update_traces(hoverinfo='label+percent', textinfo='value', 
                  textfont_size=30,
                  marker=dict(colors=colors, line=dict(color='white', width=3)))

#views
views = go.Figure(data=[go.Pie(labels=["Total Views from Control Campaign","Total Views from Test Campaign"], 
                       values=[ab_data[ab_data['Campaign name']=='Test Campaign']['Views'].sum(), 
                               ab_data[ab_data['Campaign name']=='Control Campaign']['Views'].sum()],
                      )])
colors = ['purple', 'olive']
views.update_layout(title_text='Control Vs Test: Views')
views.update_traces(hoverinfo='label+percent', textinfo='value', 
                  textfont_size=30,
                  marker=dict(colors=colors, line=dict(color='white', width=3)))

#a2c
a2c = go.Figure(data=[go.Pie(labels=["Total A2C from Control Campaign","Total A2C from Test Campaign"], 
                       values=[ab_data[ab_data['Campaign name']=='Test Campaign']['Add to cart'].sum(), 
                               ab_data[ab_data['Campaign name']=='Control Campaign']['Add to cart'].sum()],
                      )])
colors = ['tomato', 'midnightblue']
a2c.update_layout(title_text='Control Vs Test: Add to cart')
a2c.update_traces(hoverinfo='label+percent', textinfo='value', 
                  textfont_size=30,
                  marker=dict(colors=colors, line=dict(color='white', width=3)))

#number_of_purchases
number_of_purchases = go.Figure(data=[go.Pie(labels=["Total Number of purchases from Control Campaign","Total Number of purchases from Test Campaign"], 
                       values=[ab_data[ab_data['Campaign name']=='Test Campaign']['Number of purchases'].sum(), 
                               ab_data[ab_data['Campaign name']=='Control Campaign']['Number of purchases'].sum()],
                      )])
colors = ['powderblue', 'navy']
number_of_purchases.update_layout(title_text='Control Vs Test: Number of purchases')
number_of_purchases.update_traces(hoverinfo='label+percent', textinfo='value', 
                  textfont_size=30,
                  marker=dict(colors=colors, line=dict(color='white', width=3)))

#amount_spent
amount_spent = go.Figure(data=[go.Pie(labels=["Total Amount spent from Control Campaign","Total Amount spent from Test Campaign"], 
                       values=[ab_data[ab_data['Campaign name']=='Test Campaign']['Amount spent'].sum(), 
                               ab_data[ab_data['Campaign name']=='Control Campaign']['Amount spent'].sum()],
                      )])
colors = ['floralwhite', 'indigo']
amount_spent.update_layout(title_text='Control Vs Test: Amount spent')
amount_spent.update_traces(hoverinfo='label+percent', textinfo='value', 
                  textfont_size=30,
                  marker=dict(colors=colors, line=dict(color='white', width=3)))

#show all pies
searches_pie.show()
views.show()
a2c.show()
number_of_purchases.show()
amount_spent.show()


# # Conclusion
# 
# From the above A/B tests, we found that the control campaign resulted in more sales and engagement from the visitors. More products were viewed from the control campaign, resulting in more products in the cart and more sales. But the conversation rate of products in the cart is higher in the test campaign. The test campaign resulted in more sales according to the products viewed and added to the cart. And the control campaign results in more sales overall. So, the Test campaign can be used to market a specific product to a specific audience, and the Control campaign can be used to market multiple products to a wider audience.
# 
# Great thanks to Aman Kharwal for datasets and for his version of the analysis <3
