# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Michigan COVID-19 Data
# 
# ## Imports

# %%
import pandas as pd
import numpy as np

import os
import glob
import requests
from bs4 import BeautifulSoup

import seaborn as sns
import matplotlib.pyplot as plt

import geopandas as gp

# %% [markdown]
# ## Michigan COVID-19 Data
# ### Download the latest COVID-19 data

# %%
michiganCovid19Url = 'https://www.michigan.gov/coronavirus/0,9753,7-406-98163_98173---,00.html'
michiganCovid19PageSoup = BeautifulSoup(requests.get(michiganCovid19Url).content)

# %% [markdown]
# Make the michigan external data directory to store the data if it isn't there already. 

# %%
externalPath = '../data/external/michiganCovid19Data/'
dir = os.path.dirname(externalPath)
if not os.path.exists(dir):
    os.makedirs(dir)

# %% [markdown]
# Download the data into the the above folder.

# %%
# Delete the existing data as michigan datetime stamps their data
michiganDataFileNames = glob.glob('../data/external/michiganCovid19Data/*')
for fileName in michiganDataFileNames:
    os.remove(fileName)


# %%
for urlHtml in michiganCovid19PageSoup.find(id='comp_115341').find_all('a'):
    url = 'https://www.michigan.gov/' + urlHtml['href']
    with open(externalPath + url.split('/')[-1],"wb") as file:
        response = requests.get(url)
        file.write(response.content)

# %% [markdown]
# ### Read the day by day Michigan covid 19 data

# %%
glob.glob('../data/external/michiganCovid19Data/Cases_and_Deaths_by_County_and_by_Date_of_Symptom_Onset_or_by_Date_of_Death*')[0]
michiganDayByDayDf = pd.read_excel(glob.glob('../data/external/michiganCovid19Data/Cases_and_Deaths_by_County_and_by_Date_of_Symptom_Onset_or_by_Date_of_Death*')[0])
#df = pd.read_excel("../data/external/michiganCovid19Data/Cases_and_Deaths_by_County_2020-11-02_706751_7.xlsx")
#df = pd.read_excel("../data/external/michiganCovid19Data/Cases_by_Demographics_Statewide_2020-11-02_706753_7.xlsx")
#df = pd.read_excel("../data/external/michiganCovid19Data/Covid-19_Tests_by_County_2020-11-02_706754_7.xlsx")
#df = pd.read_excel("../data/external/michiganCovid19Data/Diagnostic_Tests_by_Result_and_County_2020-11-02_706755_7.xlsx")
michiganDayByDayTestingDf = pd.read_excel(glob.glob('../data/external/michiganCovid19Data/Diagnostic_Tests_by_Result_and_County*')[0])


# %%
michiganDayByDayDf

# %% [markdown]
# ### Tidy data
# Let's look to see if there is any missing data. Looks like the date data is missing.

# %%
michiganDayByDayDf.count()/michiganDayByDayDf.shape[0]

# %% [markdown]
# Since only 3 dates are missing and they don't seem impactful, let's filter out the missing date values.

# %%
michiganDayByDayDf[~np.isnat(michiganDayByDayDf["Date"])]

# %% [markdown]
# Let's look at the datatypes. Wow, it got most of them right! Let's get the CASE_STATUS and COUNTY set as category.

# %%
michiganDayByDayDf.dtypes


# %%
michiganDayByDayDf['CASE_STATUS'] = michiganDayByDayDf['CASE_STATUS'].astype('category')
michiganDayByDayDf['COUNTY'] = michiganDayByDayDf['COUNTY'].astype('category')


# %%
michiganDayByDayDf.dtypes


# %%
michiganDayByDayDf = michiganDayByDayDf[michiganDayByDayDf['CASE_STATUS'] == 'Confirmed']
michiganDayByDayDf

# %% [markdown]
# # Export Data for Final Project Notebook
# ## First export the data by county

# %%
michiganDayByDayDf["State"] = 'Michigan'


# %%
michiganExportDataFrameByCounty = michiganDayByDayDf[["Date","State","COUNTY","Cases","Deaths"]]


# %%
michiganExportDataFrameByCounty.columns=["Date","State","County","Cases","Deaths"]


# %%
michiganExportDataFrameByCounty


# %%
michiganExportDataFrameByCounty.to_csv("../data/processed/by_county/michigan.csv", index=False)

# %% [markdown]
# ## Second export by state

# %%
michiganDayByDayTestingDf.columns=["County","Date", "Negative", "Positive","Total"]
michiganDayByDayTestingDf.groupby(["Date"]).sum()


# %%
michiganExportDataFrameByState = michiganExportDataFrameByCounty.groupby("Date").sum()


# %%
michiganExportDataFrameByState["State"] = "Michigan"


# %%
michiganExportDataFrameByState


# %%
groupedTestingByDate = michiganDayByDayTestingDf.groupby("Date").sum()


# %%
groupedTestingByDate


# %%
michiganExportDataFrameByState = michiganExportDataFrameByState.merge(groupedTestingByDate,left_index=True,right_index=True)


# %%
michiganExportDataFrameByState = michiganExportDataFrameByState[["State","Cases","Positive","Negative","Deaths"]]


# %%
michiganExportDataFrameByState.to_csv("../data/processed/by_state/michigan.csv")


# %%



