# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gp


# %%
californiaCasesDeathsDf = pd.read_csv("https://data.ca.gov/dataset/590188d5-8545-4c93-a9a0-e230f0db7290/resource/926fd08f-cc91-4828-af38-bd45de97f8c3/download/statewide_cases.csv", low_memory=False)
californiaTestingTotalDf = pd.read_csv("https://data.ca.gov/dataset/efd6b822-7312-477c-922b-bccb82025fbe/resource/b6648a0d-ff0a-4111-b80b-febda2ac9e09/download/statewide_testing.csv", low_memory=False)
californiaTestingPositiveDf = pd.read_csv("https://covidtracking.com/data/download/california-history.csv", usecols=["date","positive"], low_memory=False)


# %%
toCountyDf = californiaCasesDeathsDf.copy()
toCountyDf["State"] = "California"
toCountyDf = toCountyDf[["date", "State", "county", "newcountconfirmed", "newcountdeaths"]]
toCountyDf.rename(columns={"date" : "Date", "State" : "State", "county" : "County", "newcountconfirmed" : "Cases", "newcountdeaths" : "Deaths"}, inplace=True)
toCountyDf.to_csv('../data/processed/by_county/CA.csv', index=False)


# %%
californiaTestingTotalDf.rename(columns={"date" : "Date", "tested" : "Tests"}, inplace=True)
californiaTestingPositiveDf.rename(columns={"date" : "Date", "positive" : "Positive"}, inplace=True)
californiaTestingDf = californiaTestingPositiveDf.merge(californiaTestingTotalDf)
californiaTestingDf["Negative"] = californiaTestingDf["Tests"] - californiaTestingDf["Positive"]
californiaTestingDf.drop(columns="Tests", inplace=True)


# %%
firstRow = californiaTestingDf.tail(1)
positiveDiff = californiaTestingDf.Positive.diff(periods=-1)
positiveDiff.iloc[-1] = firstRow["Positive"].values[0]
californiaTestingDf["Positive"] = positiveDiff


# %%
firstRow = californiaTestingDf.tail(1)
negativeDiff = californiaTestingDf.Negative.diff(periods=-1)
negativeDiff.iloc[-1] = firstRow["Negative"].values[0]
californiaTestingDf["Negative"] = negativeDiff
californiaTestingDf["State"] = "California"


# %%
californiaTestingDf.__dict__.update(californiaTestingDf.astype({"Positive": np.int64, "Negative": np.int64}).__dict__)
californiaTestingDf.merge(toCountyDf.groupby("Date").sum(), on="Date", how="outer")[::-1].to_csv('../data/processed/by_state/CA.csv', index=False)


