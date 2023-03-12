#!/usr/bin/python3
# this script will load in an XML file (based on a first parameter) and split it into two files called "output_incident.xml" and "output_audit.xml" based on tag name

# import libraries
import sys
import xml.etree.ElementTree as ElementTree
from datetime import datetime

# check that a filename was passed as a parameter
if len(sys.argv) < 2:
	print("Error! Missing argument")
	print("Usage: split.py <filename>")
	sys.exit(1)

# open the XML file
context = ElementTree.iterparse(sys.argv[1], events=('end', ))

# create the output files
incidentFilename = format("output_incident.xml")
auditFilename = format("output_audit.xml")
incidentFile = open(incidentFilename, 'wb')
auditFile = open(auditFilename, 'wb')

# write the XML header to the output files
currentDateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
incidentFile.write(("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<group split_date=\"" + currentDateTime + "\">\n").encode('utf-8'))
auditFile.write(("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<group split_date=\"" + currentDateTime + "\">\n").encode('utf-8'))

# loop through the digested file and write the data to the appropriate output file
for event, element in context:
	if element.tag == 'incident':
		incidentFile.write(ElementTree.tostring(element))
	elif element.tag == 'sys_audit':
		auditFile.write(ElementTree.tostring(element))

# write the XML footer to the output files and close the files
incidentFile.write("</group>".encode('utf-8'))
auditFile.write("</group>".encode('utf-8'))
incidentFile.close()
auditFile.close()

# print a message to the screen
print("Incident file created: " + incidentFilename)
print("Audit file created: " + auditFilename)
print("Split complete!")