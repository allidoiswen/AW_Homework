'''
PyPoll Challenge
'''

import os
import csv

# Define Variables

election_data = os.path.join('../..', 'PyPoll', 'Resources', 'election_data.csv')
output_date = os.path.join('PyPoll_output.csv')

# Initialize Variables

vote_count = {}

total_votes = 0

# Open csv File

with open(election_data) as election:

    election = csv.reader(election, delimiter = ',')

    # Skip header
    next(election)

    # Loop through election result
    for  vote in election:

        # Count Numer of Vote
        total_votes += 1

        # Result counter and store the result in a dictionary
        if vote[2] not in vote_count.keys():
            vote_count[vote[2]] = 1
        else:
            vote_count[vote[2]] += 1



# Print Results onto Terminal
print('Election Results')
print('-------------------------')
print(f'Total Votes: {total_votes}')
print('-------------------------')
for candidate in vote_count:
    name     = candidate
    vote     = vote_count[candidate]
    pct_vote = str(round(vote / total_votes, 2) * 100)[0:6]
    print(f"{name}: {pct_vote}% ({vote})")
print('-------------------------')

# Find the highest value in vote_count
winner = max(vote_count, key=vote_count.get)
print(f'Winner: {winner}')
print('-------------------------')


# # Save Output as a txt
# with open(output_date, 'w') as outputfile:

#     # Initialize csv.writer
#     csvwriter = csv.writer(outputfile, delimiter=':')

#     # Save Each Line into the output file
#     for line in output_dict:
#         csvwriter.writerow(output_dict[line].split(':'))
