# used https://towardsdatascience.com/manage-your-money-with-python-707579202203 for some code indicated by an **

import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go


# importing and reading my accounts
spend = pd.read_csv("accountActivityExport_spend.csv")
reserve = pd.read_csv("accountActivityExport_reserve.csv")
growth = pd.read_csv("accountActivityExport_growth.csv")
discover = pd.read_csv("accountActivityExport_Discover.csv")
venmo = pd.read_csv("venmo_statement.csv")

# removing transfers between my accounts (including credit card payments)
spend = spend[spend.Category != "Transfers"]
reserve = reserve[reserve.Description != "ONLINE TRANSFER TO        XXXXX4454 "]
reserve = reserve[reserve.Description != "ONLINE TRANSFER TO        XXXXX4438 "]
growth = growth[growth.Description != "ONLINE TRANSFER FROM      XXXXX4446 "]
growth = growth[growth.Description != "ONLINE TRANSFER FROM      XXXXX4438 "]
venmo = venmo[venmo.Type != "Standard Transfer"]
spend = spend[spend.Category != "Credit Card Payments"]
discover = discover[discover.Category != "Payments and Credits"]

# Deleting columns to make the statements match for merging
spend = spend.drop(["Withdrawals", "Deposits", "Balance"], axis=1)
reserve = reserve.drop(["Withdrawals", "Deposits", "Balance"], axis=1)
growth = growth.drop(["Withdrawals", "Deposits", "Balance"], axis=1)
venmo = venmo.drop(["ID", "Type", "Status", "From", "To", "Funding Source", "Destination"], axis=1)
discover = discover.drop(["Post Date"], axis=1)

# Making credit card charges match bank statement for negativity
discover['Amount'] = discover['Amount'].multiply(-1)

# ** Changing categories of expenses
spend['Category'] = np.where(spend['Category'].str.contains('Cable'), 'Verizon', spend['Category'] )
spend['Category'] = np.where(spend['Category'].str.contains('Personal'), 'Personal', spend['Category'] )
spend['Category'] = np.where(spend['Category'].str.contains('Merchandise'), 'Merchandise', spend['Category'] )
spend['Category'] = np.where(spend['Description'].str.contains('TARGET'), 'Personal', spend['Category'] )
reserve['Description'] = np.where(reserve['Description'].str.contains('MEIJIAO ZHENG'), 'Rent', reserve['Description'] )
reserve['Description'] = np.where(reserve['Description'].str.contains('LANA R SCHAFER'), 'Stipend', reserve['Description'] )
discover['Category'] = np.where(discover['Category'].str.contains('Supermarkets'), 'Groceries', discover['Category'] )
discover['Category'] = np.where(discover['Category'].str.contains('Services'), 'Subscriptions', discover['Category'] )
discover['Description'] = np.where(discover['Description'].str.contains('CVS'), 'CVS', discover['Description'] )
discover['Description'] = np.where(discover['Description'].str.contains('WALGREEN'), 'WALGREEN', discover['Description'] )
discover['Description'] = np.where(discover['Description'].str.contains('SPOTIFY'), 'SPOTIFY', discover['Description'] )
discover['Description'] = np.where(discover['Description'].str.contains('NETFLIX'), 'NETFLIX', discover['Description'] )
discover['Description'] = np.where(discover['Description'].str.contains('AMAZON|AMZN'), 'AMAZON', discover['Description'] )
discover['Description'] = np.where(discover['Description'].str.contains('TARGET.COM'), 'TARGET.COM', discover['Description'] )
discover['Description'] = np.where(discover['Description'].str.contains('WALMART.COM'), 'WALMART.COM', discover['Description'] )
venmo['Note'] = np.where(venmo['Note'].str.contains('Verizon'), 'Verizon', venmo['Note'] )
venmo['Note'] = np.where(venmo['Note'].str.contains('insurance|Insurance'), 'Insurance', venmo['Note'] )
venmo['Note'] = np.where(venmo['Note'].str.contains('peco|PECO|heat'), 'Electric', venmo['Note'] )
venmo['Note'] = np.where(venmo['Note'].str.contains('wraps|Cheese|chicken|cake|Ben|Dinner|Beveragino|Chicken|ingredients|groceries'), 'Groceries', venmo['Note'] )
venmo['Note'] = np.where(venmo['Note'].str.contains('bahn mi|Saxby|crepe|puyero|cofy|Philly|Sev|goldie'), 'Restaurants', venmo['Note'] )
venmo['Note'] = np.where(~venmo['Note'].str.contains('Verizon|Insurance|Electric|Groceries|Restaurants'), 'Merchandise', venmo['Note'] )

# Adding Category columns to reserve, growth, and venmo in prep for merge
venmo["Category"] = venmo["Note"]
venmo.rename(columns={"Note": "Description"}, inplace=True)
venmo.rename(columns={"Datetime": "Date"}, inplace=True)
reserve["Category"] = reserve["Description"]
growth["Category"] = growth["Description"]
discover.rename(columns={"Trans. Date": "Date"}, inplace=True)

# Adding a column to each account that says which account it is in prep for merge
spend["Account"] = 'Spend'
discover["Account"] = 'Discover'
growth["Account"] = 'Growth'
reserve["Account"] = 'Reserve'
venmo["Account"] = 'Venmo'


# Making the dates read correctly
spend["Date"] = pd.to_datetime(spend['Date']).dt.strftime('%m/%Y')
discover["Date"] = pd.to_datetime(discover['Date']).dt.strftime('%m/%Y')
growth["Date"] = pd.to_datetime(growth['Date']).dt.strftime('%m/%Y')
reserve["Date"] = pd.to_datetime(reserve['Date']).dt.strftime('%m/%Y')
venmo["Date"] = pd.to_datetime(venmo['Date']).dt.strftime('%m/%Y')

# Merging all accounts into one sheet
frames = [spend, discover, venmo, reserve, growth]
merged = pd.concat(frames)
merged.sort_values(by=['Date'], inplace = True)
merged.to_csv('merged.csv', index = False)

# ** Creating expense charts
df = merged[merged.Category != "Paychecks"]
df = df[df.Category != 'Stipend']
df.Amount = df.Amount*(-1)
Total_Monthly_Expenses_Table = df.groupby('Date')['Amount'].sum().reset_index(name = 'sum')
Total_Monthly_Expenses_Chart = px.bar(Total_Monthly_Expenses_Table, x = "Date", y = "sum", title = "Total Monthly Expenses")
Total_Monthly_Expenses_Chart.update_yaxes(title = 'Expenses ($)', visible = True, showticklabels = True)
Total_Monthly_Expenses_Chart.update_xaxes(title = 'Date', visible = True, showticklabels = True)
Total_Monthly_Expenses_Chart.show()
Expenses_Breakdown_Table = pd.pivot_table(df, values = ['Amount'], index = ['Category', 'Date'], aggfunc=sum).reset_index()
Expenses_Breakdown_Table.columns = [x.upper() for x in Expenses_Breakdown_Table.columns]
Expenses_Breakdown_Chart = px.line(Expenses_Breakdown_Table, x='DATE', y="AMOUNT", title="Expenses Breakdown", color = 'CATEGORY')
Expenses_Breakdown_Chart.update_yaxes(title='Expenses ($)', visible=True, showticklabels=True)
Expenses_Breakdown_Chart.update_xaxes(title='Date', visible=True, showticklabels=True)
Expenses_Breakdown_Chart.show()

# ** Money saved over time
Money_Saved_Table = df.groupby('Date')['Amount'].sum().reset_index(name ='sum')
Money_Saved_Table['cumulative sum'] = Money_Saved_Table['sum'].cumsum()
Money_Saved_Chart = go.Figure(
    data = go.Scatter(x = Money_Saved_Table["Date"], y = Money_Saved_Table["cumulative sum"]),
    layout = go.Layout(
        title = go.layout.Title(text = "Money Saved Over Time")
    )
)
Money_Saved_Chart.update_layout(
    xaxis_title = "Date",
    yaxis_title = "Money Saved ($)",
    hovermode = 'x unified'
    )
Money_Saved_Chart.update_xaxes(
    tickangle = 45)
Money_Saved_Chart.show()


# Discover credit card cashback
cashback_1 = 0
cashback_5 = 0
quarter1 = ['01','02','03','Groceries','CVS','WALGREEN']
quarter2 = ['04','05','06','SPOTIFY','NETFLIX']
quarter3 = ['07','08','09','Restaurants']
quarter4 = ['10','11','12','AMAZON','TARGET.COM','WALMART.COM']
for i, j in discover.iterrows():
    if j['Date'][0:2] in quarter1:
        if j['Category'] in quarter1:
            cashback_5 += 0.05 * float(j['Amount'])
        elif j['Description'] in quarter1:
            cashback_5 += 0.05 * float(j['Amount'])
        else:
            cashback_1 += 0.01 * float(j['Amount'])
    elif j['Date'][0:2] in quarter2:
        if j['Description'] in quarter2:
            cashback_5 += 0.05 * float(j['Amount'])
        else:
            cashback_1 += 0.01 * float(j['Amount'])
    elif j['Date'][0:2] in quarter3:
        if j['Category'] in quarter3:
            cashback_5 += 0.05 * float(j['Amount'])
        else:
            cashback_1 += 0.01 * float(j['Amount'])
    elif j['Date'][0:2] in quarter4:
        if j['Description'] in quarter4:
            cashback_5 += 0.05 * float(j['Amount'])
        else:
            cashback_1 += 0.01 * float(j['Amount'])

cashback_tot = cashback_5 + cashback_1
cashback_5 = str(round((-1 * cashback_5),2))
cashback_1 = str(round((-1 * cashback_1),2))
cashback_tot = str(round((-1 * cashback_tot),2))
print('5% cashback for this year is $' + cashback_5)
print('1% cashback for this year is $' + cashback_1)
print('Total cashback for this year is $' + cashback_tot)





