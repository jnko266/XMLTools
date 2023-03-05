#!/usr/bin/python3
# this script will take a filename as a parameter and then open the file and convert it to a CSV file
# the CSV file will be named the same as the input file but with a .csv extension

# import libraries
import csv
import sys
import xml.etree.ElementTree as ElementTree

# check that a filename was passed as a parameter
if len(sys.argv) < 2:
	print("Error! Missing argument")
	print("Usage: makeCSV.py <filename>")
	sys.exit(1)

# open the XML file and parse it
inputXml = ElementTree.parse(sys.argv[1])
inputXmlRoot = inputXml.getroot()

# get the set of all possible headers by iterating over all child elements
all_headers = set()
for child in inputXmlRoot:
	for subchild in child:
		tag = subchild.tag
		if tag not in all_headers:
			all_headers.add(tag)
		if subchild.attrib:
			if "/" in tag:
				all_headers.add(tag)
			for attrib in subchild.attrib.keys():
				all_headers.add(f"{tag}/{attrib}")

# create the headers by sorting the set alphabetically
headers = sorted(list(all_headers))

# create the output file (replacing the .xml extension with .csv)
csv_filename = sys.argv[1].replace('.xml', '.csv')
with open(csv_filename, "w", newline="") as csv_file:
	writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	# write the headers to the CSV file
	writer.writerow(headers)
	
	# loop through the XML file and write the data to the CSV file
	for child in inputXmlRoot:
		row = []
		for header in headers:
			tag, attrib = header.split("/") if "/" in header else (header, None)
			value = child.find(tag)
			if attrib is not None and value is not None:
				value = value.attrib.get(attrib)
			elif value is not None:
				value = value.text
			else:
				value = ""
			row.append(value)
		writer.writerow(row)
		
# close the CSV file
csv_file.close()

# print a message to the screen
print("CSV file created: " + csv_filename)
print("Conversion complete!")