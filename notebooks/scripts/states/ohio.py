
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import urllib.request
import re as re
from bs4 import BeautifulSoup
import plotly.express as ps


# %%
df = pd.read_csv("https://coronavirus.ohio.gov/static/dashboards/COVIDSummaryData.csv", low_memory=False)
# The last row is summary
df_sum = df.iloc[[-1]]
# actual data is in the other columns
df_data = df.iloc[:-1].copy()


# %%
count_columns = ["Case Count", "Death Due to Illness Count", "Hospitalized Count"]
for c in count_columns:
    df_data[c] = df_data[c].astype(int)
df_data["Onset Date"] = pd.to_datetime( df_data["Onset Date"])


# %%
cases = df_data.groupby(["Onset Date", "County"])['Case Count'].sum().reset_index()
cases["State"] = "Ohio"
cases = cases.rename(columns={"Onset Date":"Date", "Case Count":"Cases"})
# cases = cases.set_index(["State", "Date", "County"])
cases


# %%
death_data = df_data[ df_data["Date Of Death"] != "Unknown"]
death_data = death_data[ death_data["Date Of Death"].notnull()]
death_data["Date Of Death"] = pd.to_datetime( death_data["Date Of Death"])
deaths = death_data.groupby(["Date Of Death", "County"])['Death Due to Illness Count'].sum().reset_index()
deaths["State"] = "Ohio"
deaths = deaths.rename( columns={"Date Of Death":"Date", "Death Due to Illness Count":"Deaths"})
# deaths = deaths.set_index(["State", "Date", "County"])
deaths


# %%
total_data = pd.merge(cases, deaths, left_on=["State", "Date", "County"], right_on=["State", "Date", "County"])
total_data.to_csv("../data/processed/by_county/ohio.csv", index=False)
total_data


# %%
# tests from https://covidtracking.com/data
df_tracker = pd.read_csv("https://covidtracking.com/data/download/all-states-history.csv")
df_tracker["date"] = pd.to_datetime(df_tracker["date"])
ohio = df_tracker[ df_tracker["state"] == "OH"].sort_values("date", ascending = True)


# %%
total_data2 = ohio[["date", "positive", "negative"]].copy()
total_data2 = total_data2.rename(columns={"date":"Date","positive":"Positive", "negative":"Negative"})
total_data2 = pd.merge( total_data2, total_data.groupby(["Date"])["Cases","Deaths"].sum(), left_on="Date", right_on="Date")
total_data2["State"] = "Ohio"
total_data2 = total_data2.fillna(0)
for c in ["Positive", "Negative", "Deaths"]:
    total_data2[c] = total_data2[c].astype(int)
total_data2["Positive"] = total_data2["Positive"].diff()
total_data2["Negative"] = total_data2["Negative"].diff()
total_data2.to_csv("../data/processed/by_state/ohio.csv", index=False)
total_data2


# %%



