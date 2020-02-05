import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

timeseries = pd.read_html("https://docs.google.com/spreadsheets/d/1UF2pSkFTURko2OvfHWWlFpDFAr1UxCBA4JLwlSP6KFo/htmlview?usp=sharing&sle=true")

cases = timeseries[0]
recovered = timeseries[1]
deaths = timeseries[2]

def clean(df):
    df.fillna(value=0,inplace=True)
    df.loc[2:,'F':] = df.loc[2:,'F':].astype('int64')
    df.loc[0,'F':] = pd.to_datetime(df.loc[0,'F':]).dt.date
    header = df.iloc[0]
    df = df[1:]
    df.columns = header
    df = df.loc[:,~df.columns.duplicated(keep='last')]
    df = df.drop(df.index[0])
    df.reset_index(inplace=True)
    df = df.drop(['index',1.0,0.0],axis=1)
    return df

def by_breakdown(df):
    d = {}
    for country in list(df['Country/Region']):
        if country not in d.keys():
            d[country] = {}
        else:
            pass
    for i in range(len(df)):
        for country in d.keys():
            if df.iloc[i,1] == country:
                d[country][df.iloc[i,0]] = list(df.iloc[i,5:])
    return d
    
def by_total(df): 
    d = {}  
    for country in list(df['Country/Region']):
        if country not in d.keys():
            d[country] = None
        else:
            pass
    for country in d.keys():
        d[country] = [sum(df[df['Country/Region'] == country].iloc[:,j]) for j in range(5, len(df.columns))]
    d['All'] = [sum(df.iloc[:,k]) for k in range(5, len(df.columns))]
    return d


cases = clean(cases)
recovered = clean(recovered)
deaths = clean(deaths)

cases_bd = by_breakdown(cases)
recovered_bd = by_breakdown(recovered)
deaths_bd = by_breakdown(deaths)
cases_tot = by_total(cases)
recovered_tot = by_total(recovered)
deaths_tot = by_total(deaths)

print(deaths_tot['All'])
