#!/usr/bin/python3
# this script will load in an XML file (based on a first parameter) and loop through it, it will then only keep those tags that are required

# import libraries
import sys
import xml.etree.ElementTree as ElementTree
from datetime import datetime

# check that a filename was passed as a parameter
if len(sys.argv) < 2:
	print("Error! Missing argument")
	print("Usage: cleanUsers.py <filename>")
	sys.exit(1)

# open the XML file
context = ElementTree.iterparse(sys.argv[1], events=('end', ))

# create the new files
userFilename = format("output_user.xml")
userFile = open(userFilename, 'wb')

# write the XML header to the new file
currentDateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
userFile.write(("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<group cleaned_date=\"" + currentDateTime + "\">\n").encode('utf-8'))

# loop through the digested file and if tag is the tag we want, put it to a new file
for event, element in context:
	if element.tag == 'x_qdsdp_bnp_candidate':
		userFile.write(ElementTree.tostring(element))
	if element.tag == 'sys_user':
		userFile.write(ElementTree.tostring(element))

# write the XML footer to the output files and close the file
userFile.write("</group>".encode('utf-8'))
userFile.close()

# print a message to the screen
print("User file created: " + userFilename)
print("Cleanup complete!")