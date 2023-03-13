#!/usr/bin/python3
# this script will take an XML filename as a parameter and will count number of tags in the root element of the XML file

# import libraries
import xml.etree.ElementTree as ET
import sys

# check that a filename was passed as a parameter
if len(sys.argv) < 2:
	print("Error! Missing argument")
	print("Usage: tagCounter.py <filename>")
	sys.exit(1)

# parse the XML file   
tree = ET.parse(sys.argv[1])
root = tree.getroot()

counts = {}

for child in root:
	if child.tag not in counts:
		counts[child.tag] = 1
	else:
		counts[child.tag] += 1

print("Counts:")
for tag, count in counts.items():
	print(f"{tag}: {count}")