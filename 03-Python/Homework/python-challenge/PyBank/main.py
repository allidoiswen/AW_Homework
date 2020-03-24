'''
PyBank Challenge
'''
import os
import csv

# define variables
budget_data = os.path.join('../..', 'PyBank', 'Resources', 'budget_data.csv')
output_date = os.path.join('PyBank_output.csv')

# Open and Read csv
with open(budget_data) as bd:
    bd_reader = csv.reader(bd, delimiter = ',')

    # Skip header
    bd_header = next(bd_reader)
    ###print(f'header row is {bd_header}')

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
            first_iteration_flag = False   #Turn off the first row flag
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
ave_pnl_delta = round(ave_pnl_delta, 2)

output_dict = {
    0 : 'Financial Analysis',
    1 : '----------------------------',
    2 : f'Total Months: {num_month}',
    3 : f'Average  Change: ${ave_pnl_delta}',
    4 : f'Greatest Increase in Profits: {greatest_profit_month} (${greatest_profit})',
    5 : f'Greatest Decrease in Profits: {greatest_loss_month} (${greatest_loss})',
}

# Print Output onto Terminal
for line in output_dict:
    print(output_dict[line])

# Save Output as a txt
with open(output_date, 'w') as outputfile:

    # Initialize csv.writer
    csvwriter = csv.writer(outputfile, delimiter=',')

    # Save Each Line into the output file
    for line in output_dict:
        csvwriter.writerow([output_dict[line]])
