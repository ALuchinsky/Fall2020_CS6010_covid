# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # COVID-19 Statistics for Indiana
# %% [markdown]
# ## Imports

# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gp

# %% [markdown]
# ## Constants

# %%
indianaCaseDataUrl = "https://hub.mph.in.gov/dataset/bd08cdd3-9ab1-4d70-b933-41f9ef7b809d/resource/afaa225d-ac4e-4e80-9190-f6800c366b58/download/covid_report_county_date.xlsx"
indianaCaseDataDictUrl= "https://hub.mph.in.gov/dataset/bd08cdd3-9ab1-4d70-b933-41f9ef7b809d/resource/5ff3931f-aa68-4ee6-ac1d-d6c5d6cca50a/download/covid_report_county_date_dictionary.xlsx"

# %% [markdown]
# ## Data Import

# %%
df = pd.read_excel(indianaCaseDataUrl)
dfDict = pd.read_excel(indianaCaseDataDictUrl)

# %% [markdown]
# ## Data Assessment

# %%
df

# %% [markdown]
# ### Missing Data

# %%
numberOfRows = df.shape[0]
100 * (numberOfRows - df.count()) / numberOfRows

# %% [markdown]
# No missing data means we don't need to drop data or impute values.
# %% [markdown]
# ### Dataframe column data types

# %%
df.dtypes

# %% [markdown]
# #### Fix incorrect column data types

# %%
df.DATE = pd.to_datetime(df.DATE)
df.COUNTY_NAME = df.COUNTY_NAME.astype('category')

# %% [markdown]
# ### Updated column data types

# %%
df.dtypes


# %%
df.COVID_COUNT.sum()


# %%
df[['COUNTY_NAME', 'COVID_COUNT']].groupby('COUNTY_NAME').sum('COVID_COUNT')


# %%
dailyCaseDeathIndiana = df[['DATE','COVID_COUNT','COVID_DEATHS']].groupby('DATE').sum()

# %%
df.head()


# %%
dailyCaseDeathCountyIndiana = df.groupby(['COUNTY_NAME','DATE']).sum().groupby(level=0).cumsum().reset_index()


# %%
indianaCountyGeoJSONURL = "https://raw.githubusercontent.com/deldersveld/topojson/master/countries/us-states/IN-18-indiana-counties.json"

# %% [markdown]
# Citation:
# 
# Eldersveld, D. (2020) TopoJSON Collection (Version 1.0) [Source Code]. https://github.com/deldersveld/topojson.

# %%
geoDataFrame = gp.read_file(indianaCountyGeoJSONURL)

# %%
geoDataFrame.head()

# %% [markdown]
# ## Create a county organized Covid-19 DataFrame

# %%
countyDataFrame = df.groupby(['COUNTY_NAME']).sum()

# %% [markdown]
# ## Merge GeoJSON with Covid-19 DataFrame

# %%
geoDataFrameMerged = geoDataFrame.merge(countyDataFrame, right_on="COUNTY_NAME", left_on="NAME")


# %%
geoDataFrameMerged.head(5)

# %% [markdown]
# ## Modify the DataFrame for centering labels for ease of comprehension.

# %%
geoDataFrameMerged["center"] = geoDataFrameMerged["geometry"].centroid
michiganCountyNames = geoDataFrameMerged.copy()
michiganCountyNames.set_geometry("center", inplace=True)


# %%
df['State'] = 'Indiana'


# %%
byCountyDF = df.loc[:,['DATE','State','COUNTY_NAME','COVID_COUNT','COVID_DEATHS']]


# %%
byCountyDF.rename(columns={'DATE':'Date','State':'State','COUNTY_NAME':'County','COVID_COUNT':'Cases','COVID_DEATHS':'Deaths'}, inplace=True)


# %%
byCountyDF.to_csv('../data/processed/by_county/IN.csv', index=False)


# %%
byStateDF = df.groupby(['DATE']).sum().reset_index()
byStateDF['STATE'] = 'Indiana'
byStateDF['NEGATIVE'] = byStateDF['COVID_TESTS_ADMINISTRATED'] - byStateDF['COVID_POSITIVE_TESTS_ADMIN']
byStateDF = byStateDF.loc[:,['DATE','STATE','COVID_COUNT','COVID_POSITIVE_TESTS_ADMIN','NEGATIVE','COVID_DEATHS']]


# %%
byStateDF.rename(columns={'DATE':'Date','STATE':'State','COVID_COUNT':'Cases','COVID_POSITIVE_TESTS_ADMIN':'Positive','NEGATIVE':'Negative', 'COVID_DEATHS':'Deaths'}, inplace=True)


# %%
byStateDF.to_csv('../data/processed/by_state/IN.csv', index=False)


