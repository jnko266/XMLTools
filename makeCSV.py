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

# get the list of headers by iterating over all child elements in the root tag
headers = []
for child in inputXmlRoot:
    for subchild in child:
        tag = subchild.tag
        if subchild.attrib:
            # if the tag has attributes, add a column for the tag name
            if tag not in headers:
                headers.append(tag)
            for attrib, value in subchild.attrib.items():
                header = f"{tag}/{attrib}"
                if header not in headers:
                    headers.append(header)
        else:
            if tag not in headers:
                headers.append(tag)

# create the output file (replacing the .xml extension with .csv)
csv_filename = format(sys.argv[1].replace('.xml', '.csv'))
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
            if attrib is not None:
                value = value.attrib.get(attrib)
            else:
                value = value.text
            row.append(value)
        writer.writerow(row)
        
# close the CSV file
csv_file.close()

# print a message to the screen
print("CSV file created: " + csv_filename)
print("Conversion complete!")