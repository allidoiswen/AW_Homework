'''
PyBank Challenge
'''
import os
import csv

# define variables
budget_data = os.path.join('../..', 'PyBank', 'Resources', 'budget_data.csv')

# Read csv
with open(budget_data) as bd:
    bd_reader = csv.reader(bd, delimiter = ',')

    # Skip header
    bd_header = next(bd_reader)
    print(f'header row is {bd_header}')

    # initialize variable values
    num_month = 0
    pnl = 0
    first_iteration_flag = True
    greatest_profit = 0
    greatest_loss   = 0
    all_monthly_pnl_delta = []
    
    for row in bd_reader:

        # Count Toal Number of Months in this dataset
        num_month = num_month + 1 

        # Sum Total P&L
        this_row_pnl = float(row[1])
        pnl = pnl + this_row_pnl

        # Acumulate Monthly P&L Delta
        ## Detect the first row ##
        if first_iteration_flag == True:   
            first_iteration_flag = False
            pre_pnl = this_row_pnl
        else:
            monthly_pnl_delta = this_row_pnl - pre_pnl
            all_monthly_pnl_delta.append(monthly_pnl_delta)
            # update previous PnL variable for the next row
            pre_pnl = this_row_pnl

        # greatest profits
        if this_row_pnl > greatest_profit:
            greatest_profit = this_row_pnl
            greatest_profit_month = row[0]

        # greatest loss
        if this_row_pnl < greatest_loss:
            greatest_loss = this_row_pnl
            greatest_loss_month = row[0]

    ave_pnl_delta = sum(all_monthly_pnl_delta) / (num_month-1)

    print(num_month)
    print(pnl)
    print(ave_pnl_delta)
    print(f'Greatest Increase in Profits: {greatest_profit_month} ({greatest_profit})')
    print(f'Greatest Decrease in Profits: {greatest_loss_month} ({greatest_loss})')

   


        