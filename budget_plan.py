# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 09:37:24 2023

@author: walte
"""
import tkinter as tk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os

#%% Budgeting Calculations (Ideal)

def budget_calc(who=['walt','andrea'], walt = [68000, 725, 0,300, 785, 0], andrea = [60000, 725, 650, 300, 0, 0]
                , util=100, grocery = 500,tax=0.3):
    '''
    walt = [salary, mortgage, car payment, student loans, savings, 401k/roth] 
    andrea = [salary, mortgage, car payment, student loans, savings, 401k/roth] 
    util = [130] ; default is 130 (internet, gym, phones)
    grocery = [500] ; default at 500, will adjust based on costco, gas and expreso
    '''
    data=[]
    
    col = ['person','salary', 'mortgage', 'car', 'student_loan','savings','401k_roth'] 
    
    for n,m in zip([walt,andrea],who):
        inn=[]
        inn.append(m)
        for i in range(len(walt)):
            inn.append(n[i])
        data=data+[inn]
    data=pd.DataFrame([data[0],data[1]],columns=col)
    
    data['sal_aft_tax'] = data['salary'] - data['salary']*tax
    data['monthly_expenses'] = data.loc[:,'mortgage':'401k_roth'].T.sum()
    data['remaining_monthly_sal'] = data['sal_aft_tax']/13 - data['monthly_expenses']
    data['remaining_biweekly_sal'] = data['remaining_monthly_sal']/2
    data['remaining_weekly_sal'] = data['remaining_biweekly_sal']/2
       
    print(f'Remaining Weekly Income: \n{data[["person","sal_aft_tax","monthly_expenses"]]}')
    print(f'Remaining Income: \n{data[["person", "remaining_monthly_sal","remaining_biweekly_sal","remaining_weekly_sal"]]}')

    
    df_table = data[['person','remaining_monthly_sal','remaining_biweekly_sal','remaining_weekly_sal']]
    df_table = df_table.rename(columns = {'remaining_monthly_sal':'Remaining Monthly',
                               'remaining_biweekly_sal': 'Remaining Biweekly',
                               'remaining_weekly_sal':'Weekly Remaining'})
    fig, axs =plt.subplots(1,1)
    fontsize = 10
    collabel=df_table.columns
    axs.axis('tight')
    axs.axis('off')
    the_table = axs.table(cellText=df_table.values,colLabels=collabel,loc='center')
    the_table.set_fontsize(fontsize)
    the_table.scale(1.25, 2)
    plt.tight_layout()

    return data

#%% Salary Projection
 
def salary_projection(df, years = np.arange(1,11), merit = 0.04):
    
    '''
    Calculate your salary projection throughout the years
    Does not take into consideration promotion bumps
    '''
    
    proj_df = pd.DataFrame()
    d = pd.DataFrame()
    fr = pd.DataFrame()
    
    d['salary'] = df['salary'] + df['salary'] * merit
    d['year'] = 0
    proj_df = pd.concat([proj_df,d])

    for n in years:
        df['salary_0'] = df['salary'] + df['salary'] * merit
        df[f'salary_{n}'] = df[f'salary_{n-1}'] + df[f'salary_{n-1}'] * merit
        fr['salary'] = df[f'salary_{n-1}'] + df[f'salary_{n-1}'] * merit
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

#%% Calculate Remaining Balance

def expenses():  
    '''
    Calculates all your expenses and tells you 
    how much you will have remaining in your bank account
    '''
     
    cards = ['WF', 'Discover', 'Apple', 'AmEx', 'Citi', 'Chase','Fidelity','RTG','SDFCU']
    df = pd.DataFrame({'Card':cards})
    df['Balance'] = 0
    bank = float(input(f"Bank Balance: "))
    house = float(input(f"Mortgage: "))
    loans = float(input(f"Student Loans: "))
    
    for i, row in df.iterrows():
        while True:
            card_bal = float(input(f"{row['Card']}: "))
            
            if card_bal == 0:
                    break
              
            df.loc[i, 'Balance'] += card_bal
            
    Total = df['Balance'].sum() + house + loans
    Remaining = bank - Total
    df.loc[len(df)] = ['Total', Total]
    df.loc[len(df)] = ['Balance', Remaining]
    
    print(f"Total Expenses: {df['Card'].iloc[-1]} {round(df['Balance'].iloc[-2],2)}")
    print(f"Remaining in your Bank: {df['Card'].iloc[-1]} {round(df['Balance'].iloc[-1], 2)}")
    
    return df

#%% Fidelity CSV Calculation
def fidelity_calc(dates='', walt_spend=[], andrea_cc=100):
    
    wd = r'C:\Users\walte\Documents\CC_Spending'
    cc_save=r'C:\Users\walte\Documents\CC_Spending\Fidelity_Data'

    cc_csv = [f for f in os.listdir(wd) if f.endswith('.csv')]
    cc_csv.sort(key=os.path.getctime)
    CC_data=os.path.join(wd,cc_csv[-1])
    
    wd = CC_data
    
    data = pd.read_csv(wd)
    data['Date']=pd.to_datetime(data['Date'])
    data['Amount']=data.query('Transaction=="DEBIT"')['Amount'].abs()
    name = data['Name'].str.split(' ',expand=True)

    for i,row in name.iterrows():
        if len(row[0])<=3:
            row[0]=row[0] + ' ' + row[1]
            if len(row[1])<=3:
                row[0]=row[0]+ ' ' +' '+ row[2]
    data['Name']=name[0]  
    
    data_filt= data.query(f'Date>="{dates}" & Transaction=="DEBIT"')[['Date','Name','Amount']]
    
    if len(walt_spend)>0:
        walt_spend = [x.upper() for x in walt_spend]

        rm = []
        for n in walt_spend:    
            name = [f for f in data['Name'].str.upper() if n in f][0]
            rm=rm+[name]
        i = []
        for m in rm:
            ind = data_filt[(data_filt.Name == m)].index
            i= i + [ind]
        for index in i:
            data_filt = data_filt.drop(index)
    calc = data_filt.groupby('Name',as_index=False)['Amount'].sum()
    calc.loc[0, 'Total']=calc['Amount'].sum()
    
    if andrea_cc>0:
        calc['Total']= calc['Total'].iloc[0]-andrea_cc
        calc.loc[0, 'Andrea_half']=calc['Total'].iloc[0]/2
    else:
        calc.loc[0, 'Andrea_half']=calc['Total'].iloc[0]/2
    
    print(f'Total Spent on Fidelity Card: \n{round(calc["Total"].iloc[0],2)}')
    print(f'Halfed: \n{round(calc["Andrea_half"].iloc[0],2)}')

    fig,ax=plt.subplots(1,1,figsize=(16,8))
    ax.barh(calc['Name'],calc['Amount'])

    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)
    # Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad = 5)
    ax.yaxis.set_tick_params(pad = 10)
    # Add x, y gridlines
    ax.grid(visible = True, color ='grey',
            linestyle ='-', linewidth = 0.5,
            alpha = 0.5)
    # Show top values 
    ax.invert_yaxis()
    # Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width()+0.2, i.get_y()+0.5, 
                 str(round((i.get_width()), 2)),
                 fontsize = 10, fontweight ='bold',
                 color ='grey')
    # Add Plot Title
    ax.set_title('Breakdown of Total Spent in Fidelity Credit Card since'+
                 f' {data_filt["Date"].dt.date.iloc[0]} to {data_filt["Date"].dt.date.iloc[-1]}'+
                 f'\n Spent: \n{round(calc["Total"].iloc[0],2)} \n Halfed: \n{round(calc["Andrea_half"].iloc[0],2)}',
                 loc ='left')
    plt.tight_layout()
    plt.savefig(f'{cc_save}/Graph_{data_filt["Date"].dt.date.iloc[0]}_{data_filt["Date"].dt.date.iloc[-1]}.png')

    return calc
#%% Expenses GUI 

def create_expense_tracker():
    
    '''
    User input GUI of all your household expenses
    Will calculate half of the expenses as well
    '''
    
    def save_expense_report():
        wd = r'C:\Users\walte\Documents\expense_report'
        today_date = datetime.date.today().strftime("%m%d%Y")
        df.to_csv(f'{wd}\expense_report_{today_date}.csv', index=False)

    def add_expense():
        card = card_var.get()
        balance = float(balance_var.get())
        category = category_var.get()
        
        if card == 'Total':
            return
        
        df.loc[df['Category'] == card, 'Balance'] += balance
        df.loc[df['Category'] == card, 'Comments'] = category
        
        balance_var.set("")  # Clear the balance input field
        update_dataframe_preview()

    def calculate_total():
        total = df['Balance'].sum()
        Dtotal = df['Balance'].head(6).sum()
        df.loc[len(df)] = ['Total', total, 'Total_Spent']
        df.loc[len(df)] = ['DTotal',Dtotal - df['Balance'].iloc[6], 'Minus Andreas']
        df.loc[len(df)] = ['Half_Total', (Dtotal- df['Balance'].iloc[6])/2, 'Halfed']
        update_dataframe_preview()

    def update_dataframe_preview():
        text_widget.delete(1.0, tk.END)  # Clear existing content
        text_widget.insert(tk.END, df.to_string())
        save_expense_report()

    # Create the initial DataFrame
    cards = ['Food', 'Groceries', 'Starbucks', 'Out', 'Gas', 'House', 'Andrea_expenses']
    data = {'Category': cards, 'Balance': [0] * len(cards), 'Comments': [''] * len(cards)}
    df = pd.DataFrame(data)

    # Create the main application window
    app = tk.Tk()
    app.title("Expense Tracker")

    # Set the initial window size
    app.geometry("600x400")  # Set the width and height

    # Create and configure widgets
    card_label = tk.Label(app, text="Category Name:")
    card_var = tk.StringVar()
    card_var.set(cards[0])
    card_menu = tk.OptionMenu(app, card_var, *cards)

    balance_label = tk.Label(app, text="Expense Amount:")
    balance_var = tk.StringVar()
    balance_entry = tk.Entry(app, textvariable=balance_var)

    category_label = tk.Label(app, text="Comments:")
    category_var = tk.StringVar()
    category_entry = tk.Entry(app, textvariable=category_var)

    add_button = tk.Button(app, text="Add Expense", command=add_expense)
    total_button = tk.Button(app, text="Calculate Total", command=calculate_total)

    text_widget = tk.Text(app, wrap=tk.WORD, width=50, height=10)  # Create a text widget for displaying DataFrame

    # Place widgets on the window
    card_label.grid(row=0, column=0)
    card_menu.grid(row=0, column=1)
    balance_label.grid(row=1, column=0)
    balance_entry.grid(row=1, column=1)
    category_label.grid(row=2, column=0)
    category_entry.grid(row=2, column=1)
    add_button.grid(row=3, column=0, columnspan=2)  # Span two columns
    total_button.grid(row=4, column=0, columnspan=2)  # Place the Total button
    text_widget.grid(row=5, column=0, columnspan=2)  # Place the text widget

    update_dataframe_preview()  # Display initial DataFrame content

    return app
