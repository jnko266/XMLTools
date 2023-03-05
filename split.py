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
incident_filename = format("output_incident.xml")
audit_filename = format("output_audit.xml")
incident_file = open(incident_filename, 'wb')
audit_file = open(audit_filename, 'wb')

# write the XML header to the output files
current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
incident_file.write(("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<group split_date=\"" + current_date_time + "\">\n").encode('utf-8'))
audit_file.write(("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<group split_date=\"" + current_date_time + "\">\n").encode('utf-8'))

# loop through the digested file and write the data to the appropriate output file
for event, element in context:
	if element.tag == 'incident':
		incident_file.write(ElementTree.tostring(element))
	elif element.tag == 'sys_audit':
		audit_file.write(ElementTree.tostring(element))

# write the XML footer to the output files and close the files
incident_file.write("</group>".encode('utf-8'))
audit_file.write("</group>".encode('utf-8'))
incident_file.close()
audit_file.close()

# print a message to the screen
print("Incident file created: " + incident_filename)
print("Audit file created: " + audit_filename)
print("Split complete!")