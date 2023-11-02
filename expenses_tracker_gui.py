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
    cards = ['Food', 'Groceries', 'Dining', 'Out', 'Gas', 'House', 'Andrea_expenses']
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
