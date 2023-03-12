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
allHeaders = set()
for child in inputXmlRoot:
	for subchild in child:
		tag = subchild.tag
		if tag not in allHeaders:
			allHeaders.add(tag)
		if subchild.attrib:
			if "/" in tag:
				allHeaders.add(tag)
			for attrib in subchild.attrib.keys():
				allHeaders.add(f"{tag}/{attrib}")

# create the headers by sorting the set alphabetically
headers = sorted(list(allHeaders))

# create the output file (replacing the .xml extension with .csv)
csvFilename = sys.argv[1].replace('.xml', '.csv')
with open(csvFilename, "w", newline="") as csvFile:
	writer = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

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
csvFile.close()

# print a message to the screen
print("CSV file created: " + csvFilename)
print("Conversion complete!")