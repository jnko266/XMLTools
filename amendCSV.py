#!/usr/bin/python3
# this script will take a filename as a parameter and will move the sys_id column to the first column in the CSV file

# import libraries
import csv
import sys

# check that a filename was passed as a parameter
if len(sys.argv) < 2:
	print("Error! Missing argument")
	print("Usage: amendCSV.py <filename>")
	sys.exit(1)

# open the CSV file in read-only mode
with open(sys.argv[1], 'r') as csvfile:
    # read the CSV file and get the header row
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    
	# get the index of the sys_id column and create a new header with sys_id as the first column
    sys_id_index = header.index("sys_id")
    new_header = ["sys_id"] + [col for col in header if col != "sys_id"]
    
	# create a new list of rows with sys_id data as the first column
    rows = [row for row in csvreader]
    new_rows = [[row[sys_id_index]] + [col for i, col in enumerate(row) if i != sys_id_index] for row in rows]
    
# close the CSV file
csvfile.close()

# create a new CSV file with the new header and rows
with open(sys.argv[1].replace('.csv', '_new.csv'), 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(new_header)
    csvwriter.writerows(new_rows)

# close the CSV file
csvfile.close()

print("CSV transformation complete!")