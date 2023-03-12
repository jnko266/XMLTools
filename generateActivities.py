#!/usr/bin/python3
# this script will take two filenames as a parameter and will generate activities for the records in the first file
# activities will be appended to the second file

# import libraries
import csv
import sys

# check that a filenames were passed as a parameter
if len(sys.argv) < 3:
	print("Error! Missing argument(s)")
	print("Usage: generateActivities.py <incident_filename> <audit_filename>")
	sys.exit(1)

# open the audit CSV file in read-only mode and load the header data
with open(sys.argv[2], 'r') as auditFile:
	auditReader = csv.reader(auditFile)
	auditHeaders = next(auditReader)
	if not auditHeaders:
		print(f"{sys.argv[2]} has no headers")
		sys.exit(1)
	if "activity_uf" not in auditHeaders:
		print(f"{sys.argv[2]} does NOT have activity_uf column in headers. Are you sure you are using pre-parsed audit file?")
		sys.exit(1)

# open the incident CSV file in read-only mode as well as the audit CSV file in append mode
with open(sys.argv[1], 'r') as incidentFile, open(sys.argv[2], 'a', newline='') as auditFile:
	incidentReader = csv.DictReader(incidentFile)
	auditWriter = csv.DictWriter(auditFile, fieldnames=auditHeaders)

	# loop through each row in the incident file
	for row in incidentReader:
		contactType = row['contact_type']
		openedAt = row['opened_at']
		sysId = row['sys_id']

		# create the new row for the audit file
		newRow = {
			'documentkey': sysId,
			'sys_created_on': openedAt,
			'activity_uf': f"Ticket opened using {contactType}"
		}

		# write the new row to the audit file
		auditWriter.writerow(newRow)