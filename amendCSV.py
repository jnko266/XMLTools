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

filename = sys.argv[1]

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    sys_id_index = header.index("sys_id")
    new_header = ["sys_id"] + [col for col in header if col != "sys_id"]
    rows = [row for row in csvreader]
    new_rows = [[row[sys_id_index]] + [col for i, col in enumerate(row) if i != sys_id_index] for row in rows]

new_filename = filename.split(".csv")[0] + "_new.csv"

with open(new_filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(new_header)
    csvwriter.writerows(new_rows)

print(f"Moved 'sys_id' column to first column in {filename} and saved the new file as {new_filename}")