# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 18:14:27 2019

@author: Shashank
"""

# Importing the Libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen

# Importing the Website URL
url = 'https://www.hubertiming.com/results/2018MLK'
html = urlopen(url)

# Creating Variable to store the website data
soup = BeautifulSoup(html, 'lxml')

# Extracting the information from the website
# Pulling the Title
title = soup.title
title # Pulls the title with the html title tags
title.text # Pulls the title without the html title tags
# Pulling the Links with 'href' only
links = soup.find_all('a', href = True)
for link in links:
    print(link['href'])
# Pulling the Data by rows (html tag tr)
data = []
allrows = soup.find_all('tr')
for row in allrows:
    row_list = row.find_all('td')
    dataRow = []
    for cell in row_list:
        dataRow.append(cell.text)
    data.append(dataRow)
data = data[5:]
print(data) # -2: to print the Last 2 rows of data

# Creating the Dataset
dataset = pd.DataFrame(data)
#print(dataset)
dataset.head().append(dataset.tail())

# Setting the Headers in the Dataset
header_list = []
col_headers = soup.find_all('th')
for col in col_headers:
    header_list.append(col.text)
print(header_list)
# Renaming the dataset columns
dataset.columns = header_list
dataset.info()
dataset = dataset.dropna(axis = 0, how = 'any')
dataset.shape

# Creating a Column to store Chip_Time in minutes
date = []
for i in range(0, 152):
    date1 = ('00:' + dataset['Chip Time'][i])
    date.append(date1)
df = pd.DataFrame(date)
df.columns = ['ChipTime_minutes']
df = pd.Timestamp(df['ChipTime_minutes'])
for i in range(0, 152):
    dataset['Chip Time'][i] = df.iloc[:, 0][i]

dataset['ChipTime_Minutes'] = pd.to_timedelta(dataset['Chip Time'].dt.days, unit = 'd')
dataset.iloc[:, 14] = dataset.iloc[:, 14] - pd.to_timedelta(dataset.iloc[:, 14].dt.days, unit = 'd')
dataset['ChipTime_Minutes'].head().append(dataset['ChipTime_Minutes'].tail())
dataset['ChipTime_Minutes'] = dataset['ChipTime_Minutes'].dt.total_seconds() / 60

# Exploring the Dataset created
plt.bar(dataset['Gender'], dataset['ChipTime_Minutes'])
dataset.describe(include = [np.number])

dataset.boxplot(column = 'ChipTime_Minutes', by = 'Gender')
plt.ylabel('Run Time')

plt.scatter(dataset['ChipTime_Minutes'], dataset['Age'])
plt.show()