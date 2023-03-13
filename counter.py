#!/usr/bin/python3
# this script will take an XML filename as a parameter and will count number of tags in the root element of the XML file

# import libraries
import xml.etree.ElementTree as ET
import csv
import sys
import os

# check that a filename was passed as a parameter
if len(sys.argv) < 2:
	print("Error! Missing argument")
	print("Usage: tagCounter.py <filename>")
	sys.exit(1)

# get file extension
fileExt = os.path.splitext(sys.argv[1])[1]

if fileExt == ".xml":
	# parse the XML file   
	tree = ET.parse(sys.argv[1])
	root = tree.getroot()

	# loop through child records and count them
	counts = {}
	for child in root:
		if child.tag not in counts:
			counts[child.tag] = 1
		else:
			counts[child.tag] += 1

	# print result
	print("Counts:")
	for tag, count in counts.items():
		print(f"{tag}: {count}")


elif fileExt == ".csv":
	# open the CSV file in read-only mode and count rows (excluding header)
	with open(sys.argv[1], 'r') as f:
		reader = csv.reader(f)
		header = next(reader)
		numRows = sum(1 for row in reader)

	# print result
	print(f"Number of rows (excluding header): {numRows}")