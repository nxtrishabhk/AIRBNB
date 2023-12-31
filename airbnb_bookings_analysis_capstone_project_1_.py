# -*- coding: utf-8 -*-
"""Airbnb Bookings Analysis  - Capstone Project 1 .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1G67vGPRrGJQW7ZkPR4MYmDF9GxER-To9

## <b> Since 2008, guests and hosts have used Airbnb to expand on traveling possibilities and present a more unique, personalized way of experiencing the world. Today, Airbnb became one of a kind service that is used and recognized by the whole world. Data analysis on millions of listings provided through Airbnb is a crucial factor for the company. These millions of listings generate a lot of data - data that can be analyzed and used for security, business decisions, understanding of customers' and providers' (hosts) behavior and performance on the platform, guiding marketing initiatives, implementation of innovative additional services and much more. </b>

## <b>This dataset has around 49,000 observations in it with 16 columns and it is a mix between categorical and numeric values. </b>

## <b> Explore and analyze the data to discover key understandings (not limited to these) such as :
* What can we learn about different hosts and areas?
* What can we learn from predictions? (ex: locations, prices, reviews, etc)
* Which hosts are the busiest and why?
* Is there any noticeable difference of traffic among different areas and what could be the reason for it? </b>

# **Airbnb EDA Project**

**Airbnb is an online marketplace connecting travelers with local hosts. On one side, the platform enables people to list their available space and earn extra income in the form of rent. On the other, Airbnb enables travelers to book unique homestays from local hosts, saving them money and giving them a chance to interact with locals. Catering to the on-demand travel industry, Airbnb is present in over 190 countries across the world.**

This dataset has 48895 observations in it with 16 columns and it is a mix between categorical and numeric values.

1. id : Column id is a unique column in the dataset
2. name : This column contains the name of the listing.
3. host_id : This column contains the host IDs of the various hosts. Each host has a unique host ID.
4. host_name : This column contains the name of the hosts for a listing.
5. neighbourhood_group : It is an categorical column containg different neighbourhood groups.
6. neighbourhood : It is an categorical column containg the various neighbourhoods of a listing.
7. lattitude : It is an numerical column containg the latitude of the geographical location of the listing.
8. longitude : It is an numerical column containg the longitude of the geographical location of the listing.
9. room_type : It is an categorical column containg different room types.
10. price : This column contains the price of the listings.
11. minimum_nights : It contains the minimum number of nights spend by tourists in a listing.
12. number_of_reviews : This column shows how many reviews are there for a particular listings.
13. last_review : This column contains the last date when the listing was reviewed.
14. reviews_per_month : This column contains the number of reviews for a particular listing in a month.
15. calculated_host_listings_count : This column shows number of listings of a particular host.
16. avalaibility_365 : This column shows the avalaibilty of a listing on yearly basis.

## **Importing Libraries**
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
from wordcloud import WordCloud
warnings.filterwarnings('ignore')

"""## **Mounting the Drive**"""

from google.colab import drive
drive.mount('/content/drive')

"""## <b> Loading the Dataset"""

df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/EDA/Airbnb NYC 2019.csv')

df.head()

"""## <b>  Print the Info

To get the data types and non_null values
"""

df.info()

"""## <b> Droping the uneccessary columns"""

df.drop(['host_name'], axis=1, inplace=True)

"""## <b>Checking the duplicate value and remowing it if any"""

df.duplicated().sum()
df.drop_duplicates(inplace=True)

"""##<b> Check for the null values in each column"""

df.isnull().sum()

"""**as 'last_review', 'reviews_per_month' columns having more than 20% of the data missing we will drop these columns**"""

df.drop(['last_review','reviews_per_month'], axis=1, inplace=True)

df.info()

# We are setting index as id column
df= df.set_index('id')

"""## <b> Examing the changes in dataset"""

df.head()

df.shape

## It is an id column so it can not be of numerical type
df['host_id'] = df['host_id'].astype(str)

"""### **Brief information about numerical columns in our dataset**"""

## as the values of our columns are abruptly chanaging from 75% to 100% we divided it into small buckets
df.describe(percentiles = [.25,.50,.75,.80,.85,.90,.95])

"""**we can observe that the minimum price is zero that is unjustified**"""

#checking the number of rows with price = 0
len(df[df['price'] ==0])

# as the prices of these Airbnb's are zero these are unjustified also their number is insignificant in the analysis
df = df[df['price']!= 0]

"""### **For Categorical Columns**"""

for i in ['room_type','neighbourhood_group','neighbourhood']:
    print(i,':',df[i].nunique())
    print(pd.unique(df[i]))

"""### **Plotting the correlation matrix**"""

sns.set(rc={'figure.figsize':(11.7,8.27)})
sns.heatmap(df.corr(), cmap="YlGnBu", annot=True)

"""**All columns are numerically independent according to the correlation matrix**

## **Distribution of categorical columns**

## **neighbourhood_group**

Plotting the count plot of different neighbourhod_group
"""

sns.countplot(df['neighbourhood_group'], palette="magma")
fig = plt.gcf()
fig.set_size_inches(10,10)
plt.title('Neighbourhood Group')

"""*Most of the properties are located in Manhattan and Brooklyn follwed by Queens, Bronx and Staten Island respectively.*

## **neighbourhood**

**to increase the readability of the neighbourhood count plots ,each plot was created based on their respective neighbourhood_group category**
"""

for i in df['neighbourhood_group'].unique():

  sns.countplot(df[df['neighbourhood_group']== i]['neighbourhood'], palette="plasma")
  fig = plt.gcf()
  fig.set_size_inches(25,6)
  plt.title('Neighbourhood: ' + str(i))
  plt.tick_params(axis='x', rotation=90)
  plt.show()

"""## **room_type**"""

vc = pd.DataFrame((df['room_type'].value_counts(normalize = True ) * 100) )
fig, ax = plt.subplots()
labels = vc.index.tolist()
percentages = vc.room_type.tolist()
explode=(0,0,0.1)
ax.pie(percentages,explode = explode, labels = labels,autopct='%1.0f%%')
ax.set_title("Room Type")
ax.legend(frameon=False, bbox_to_anchor=(1.5,0.8))

"""*The Entire home / apt and Private room as room type have the most number of count and Shared room has the least.*

# **Now the distributions plot for each of the numerical coloumns are as follows**
"""

for i in df.columns:
  if df[i].dtype != 'object':
    sns.distplot(df[i])
    plt.show()

"""# **What is the average price based on location and room type?**"""

average_price_df = pd.DataFrame(df.groupby(['neighbourhood_group','room_type'])['price'].mean().unstack())
average_price_df

average_price_df.plot.bar()
sns.set(rc={'figure.figsize':(10,8)})
plt.show()

"""*From the mean price we can observe the average prices for Entire home/apt is the most but there is no significant difference between the prices of Shared room and Private Room in most of the neighbourhood_group*

## **Minimum and Maximum prices in different neighbourhood according to room type**
"""

min_and_max_df = pd.DataFrame(df.groupby(['neighbourhood_group','room_type'])['price'].describe()[['min','max']].unstack())
min_and_max_df

"""*The min price for entire home / apt as room type in Manhattan and Brooklyn is \$10 and maximum goes upto \$10000.*  

*For each room type the mean price for Manhattan is the most which makes it the most expensive place to stay.*

# **Find the total count of each room type according to neighbourhood_group**
"""

count_room_type = pd.DataFrame(df.groupby(['neighbourhood_group'])['room_type'].value_counts().unstack())
count_room_type

count_room_type.plot.bar()
plt.show()

"""*Manhattan has the maximum number of Entire home / apt as room_type and Brooklyn has the maximum number of Private room.*

# **Find the relationship between neighbourhood group and availability of rooms**
"""

avalaibilty_df = pd.DataFrame(df.groupby(['neighbourhood_group','room_type'])['availability_365'].median().unstack()).astype('int')
avalaibilty_df

avalaibilty_df.plot.bar()
plt.show()

"""*The avalaibilty of all room types is relatively low in Manhattan hence it is the most occupied neighborhood of NYC*

# **Plotting the scatter plot of avalaibilty according to longitude and latitude**
"""

sns.scatterplot(df.longitude,df.latitude,hue=df.availability_365)
plt.ioff()

"""# **Plotting the scatter plot of neighbourood_group according to longitude and latitude**"""

sns.scatterplot(df.longitude,df.latitude,hue=df.neighbourhood_group)
plt.ioff()

"""# **Average number of nights stay in every room type in neighbourhood**"""

nights_stays_df = pd.DataFrame(df.groupby(['neighbourhood_group','room_type'])['minimum_nights'].mean().unstack())
nights_stays_df

nights_stays_df.plot.bar()
plt.show()

"""## **Top 10 hosts according to count of listings**"""

count_host_id = pd.DataFrame(df['host_id'].value_counts())
count_host_id = count_host_id.reset_index().rename(columns = {'host_id': 'count', 'index' : 'host_id'})
count_host_id.head(10)

# Plotting the bar graph
data = count_host_id.head(10)
sns.set(rc={'figure.figsize':(10,8)})
sns.set_style('white')
viz_bar = sns.barplot(x= 'host_id', y= 'count', color='g', data=data, order=data.sort_values('count',ascending = False).host_id)
viz_bar.set_title('Hosts with most listings')
viz_bar.set_xlabel('Host ID')
viz_bar.set_ylabel('Count of host listings')
plt.tick_params(axis='x', rotation=45)
plt.show()

"""*The host with maximum listings have 327 listings with host id 219517861*

# **Top 10 highest listing neighbourhood**
"""

count_neighbourhood = pd.DataFrame(df['neighbourhood'].value_counts())
count_neighbourhood = count_neighbourhood.reset_index().rename(columns = {'neighbourhood': 'count', 'index' : 'neighbourhood'})
count_neighbourhood = count_neighbourhood.merge(df[['neighbourhood', 'neighbourhood_group']].drop_duplicates(keep = 'first'),on = 'neighbourhood', how = 'left')
count_neighbourhood[['neighbourhood_group','neighbourhood', 'count']].head(10)

data = count_neighbourhood[['neighbourhood', 'count']].head(10)
sns.set_style('white')
viz_bar = sns.barplot(x= 'neighbourhood', y= 'count', color='g', data=data, order=data.sort_values('count',ascending = False).neighbourhood)
viz_bar.set_title('Top 10 highest listing neighborhood')
viz_bar.set_xlabel('Neighbourhood')
viz_bar.set_ylabel('Count of Airbnb')
plt.tick_params(axis='x', rotation=45)
plt.show()

"""*Williamsburg  have the most number of listing in a particular neighbourhood.*
  
*In Manhattan, Harlem has the most number of listing.*

## **Word Cloud**

*To find the most used words in name of listings.*
"""

# joining all the name of listings to form a string
text =  df['name'].str.cat(sep=' ')

# remowing the stop words
import re
txt = re.sub('[^A-Za-z ]+', ' ', text)
txt = " ".join(txt.split())

plt.subplots(figsize=(25,15))
wordcloud = WordCloud(
                          background_color='white',
                          width=1920,
                          height=1080
                         ).generate(txt)
plt.imshow(wordcloud)
plt.axis('off')
plt.savefig('neighbourhood.png')
plt.show()

"""## **Conclusions**

* Manhattan is the most emphasised area in New York for hosting.
* The most popular room type is 'Entire home/apt,' with 52 percent of listings, and the least popular is 'Shared Room,' with only 2.4 percent of listings.
* The average price for an entire home/apt is the highest, but there is no notable difference between the pricing of a Shared room and a Private Room in most of the neighborhood groups.
* In every neighbourhood, people stay in the entire home / apt room type for longer periods of time.
* Since the avalaibilty of Entire home/apt and Private room is relatively low in Manhatttan new hosts should invest in these room type.
* The properties are usually described in the listing's name.
"""