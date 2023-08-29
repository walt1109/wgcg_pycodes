"""
Created on Mon Jul 31 09:37:24 2023

@author: walte
"""

import sys
sys.path.insert(1, r'C:\Users\walte\Documents\Python_Scripts')

from budget_plan import *

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
    
def budget_df(col=['who','salary'], sal = [55500,53000]):

    data = [['Walter', sal[0]], ['Andrea', sal[1]]]
    d = pd.DataFrame(data=data,columns=col)
    
    return d
    
    
    
def budget_calc(df, mort=675, util=125, grocery = 500, saving = 785, roth_401k = 118.2):
    
    mont_sav = saving*2
    sal_tax = df['salary'] - df['salary']*(0.078)
    mon_sal = (sal_tax/52)*4
    
    df['remaining_monthly_sal'] = mon_sal - (
        mont_sav + grocery + util + mort + roth_401k)
                            
    df['remaining_biweekly_sal'] = df['remaining_monthly_sal']/2
    df['remaining_weekly_sal'] = df['remaining_biweekly_sal']/2
    
    print(f'Remaining Monthly Income: \n{df["remaining_monthly_sal"]}')
    print(f'Remaining Bi-weekly Income: \n{df["remaining_biweekly_sal"]}')
    print(f'Remaining Weekly Income: \n{df["remaining_weekly_sal"]}')
    
    return df
    
def salary_projection(df, years = np.arange(1,11), merit = 0.04):
    proj_df = pd.DataFrame()
    d = pd.DataFrame()
    fr = pd.DataFrame()
    
    d['salary'] = df['salary'] + df[f'salary'] * merit
    d['year'] = 0
    proj_df = pd.concat([proj_df,d])

    for n in years:
        df['salary_0'] = df['salary'] + df[f'salary'] * merit
        df[f'salary_{n}'] = df[f'salary_{n-1}'] + df[f'salary_{n-1}'] * merit
        fr[f'salary'] = df[f'salary_{n-1}'] + df[f'salary_{n-1}'] * merit
        fr['year'] = n
        proj_df = pd.concat([proj_df,fr])

    plot = plt.plot(proj_df.groupby('year').head(1)['year'], proj_df.groupby('year').head(1)['salary'], label='Walter')
    plt.xlabel('Years')
    plt.ylabel('Salary')
    plt.title(f'Salary Grown in {n} Years')
    plt.legend(loc="upper left")
    plot = plt.plot(proj_df.groupby('year').tail(1)['year'], proj_df.groupby('year').tail(1)['salary'], c = 'r',label='Andrea')
    plt.legend(loc="upper left")
    
    pl = proj_df.groupby('year', as_index=False).head(1)
    pla = proj_df.groupby('year', as_index=False).tail(1)

    for i, row in pl.iterrows():
        plt.axhline(row['salary'], alpha=0.5)
    for i, row in pla.iterrows():
        plt.axhline(row['salary'], alpha = 0.5, color='r')
    plot = plot
    
    return plot



