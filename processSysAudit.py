#!/usr/bin/python3
# this script will take a filename as a parameter and then parse the sys_audit file to create a user-friendly readable activities column
# it is expected that the filename is a CSV file and that the CSV file has the following columns (headers):
# - fieldname
# - oldvalue
# - newvalue

# import libraries
import sys
import csv

# check that a filename was passed as a parameter
if len(sys.argv) < 2:
	print("Error! Missing argument")
	print("Usage: processSysAudit.py <filename>")
	sys.exit(1)

# define a list of fieldnames that this script "knows" how to handle (script will then display those that are not contained in this list to the user for manual review)
knownFieldNames = ["closed_at", "incident_state", "state", "active", "closed_by", "follow_up", "u_follow_up_count", "close_code", "close_notes", "assigned_to", "business_duration", "hold_reason", "business_stc", "u_resolution_subcategory", "calendar_stc", "calendar_duration", "u_resolution_category", "resolved_at", "comments", "resolved_by", "work_notes", "category", "description", "priority", "subcategory", "urgency"]

# define a list of fieldnames that we don"t need (entire row will be ignored if the fieldname is in this list)
ignoredFieldNames = ["DELETED", "closed_at", "incident_state", "closed_by", "follow_up", "u_follow_up_count", "close_code", "business_duration", "business_stc", "u_resolution_subcategory", "calendar_stc", "calendar_duration", "u_resolution_category", "resolved_at", "resolved_by"]

# define an empty list to hold the fieldnames that are not in the knownFieldNames list
unknownFieldNames = []

# define a function that gets fieldname value as a parameter, alongside oldvalue and newvalue and returns activity_uf, which will get added to the CSV as a new column
def get_activity_value(fieldName, oldValue = "", newValue = ""):
	match fieldName:
		case "closed_at":
			return "Incident closed"
		case "comments":
			if oldValue == "JOURNAL FIELD ADDITION":
				return "New comment added"
			else:
				return ""
		case "work_notes":
			if oldValue == "JOURNAL FIELD ADDITION":
				return "New comment added"
			else:
				return ""
		case "state":
			if newValue == "7":
				return "Incident closed"
			elif newValue == "6":
				return "Incident resolved"
			elif newValue == "3":
				return "Incident on hold"
			elif newValue == "4":
				return "Status - customer updated"
			elif newValue == "13":
				return "Status - assigned"
			else:
				return "Incident state changed - UNDEFINED"
		case "active":
			if newValue == "1":
				return "Incident active"
			elif newValue == "0":
				return "Incident inactive"
			else:
				return "Incident activity changed - UNDEFINED"
		case "close_notes":
			if newValue not in ["Auto-resolved, no response from the Caller.", "This incident has been resolved by Virtual Agent.", "Closed/Resolved by Caller via SelfService"]:
				return "Custom close note added"
			else:
				return -1
		case "assigned_to":
			if oldValue == "":
				return "Incident assigned to a new operative"
			elif newValue == "":
				return "Incident unassigned from operative"
			else:
				return "Incident assigned to a different operative"
		case "hold_reason":
			if oldValue == "1":
				return "Incident no longer on hold"
			elif newValue == "1":
				return "Incident placed on hold"
		case "category":
			return "Incident category changed"
		case "description":
			return "Incident description changed"
		case "priority":
			if newValue < oldValue:
				return "Incident priority increased"
			elif newValue > oldValue:
				return "Incident priority decreased"
			else:
				return "Incident priority changed - UNDEFINED"
		case "subcategory":
			return "Incident subcategory changed"
		case "urgency":
			if newValue < oldValue:
				return "Incident urgency increased"
			elif newValue > oldValue:
				return "Incident urgency decreased"
			else:
				return "Incident urgency changed - UNDEFINED"
			
	return "Unhandled fieldname - UNDEFINED"

# open the CSV file and create a reader object
with open(sys.argv[1], "r") as csvFile:
	csvReader = csv.DictReader(csvFile)

	# add a new "activity_uf" column to the header row
	header = csvReader.fieldnames + ["activity_uf"]

	# create a list to store the new rows
	newRows = []

	# iterate over the data rows and create a new column with the activity_uf value
	for row in csvReader:
		fieldname = row["fieldname"]

		# check if fieldname is in the list of known fieldnames AND not in the list of ignored fieldnames
		if fieldname in knownFieldNames:
			if fieldname not in ignoredFieldNames:
				updatedRow = row
				oldvalue = row["oldvalue"]
				newvalue = row["newvalue"]
				activity_uf_value = get_activity_value(fieldname, oldvalue, newvalue)

				# if activity_uf_value is not -1, then add it to the updatedRow dictionary and append the updatedRow to the newRows list (-1 means that the activity_uf_value is not needed)
				if activity_uf_value != -1:
					updatedRow["activity_uf"] = activity_uf_value
					newRows.append(updatedRow)
		else:
			# if fieldname is not in the list of known fieldnames, then add it to the unknownFieldNames list
			unknownFieldNames.append(fieldname)

	# remove duplicates from the unknownFieldNames list and alphabetize the list
	unknownFieldNames = sorted(list(set(unknownFieldNames)))

	# write the new rows to a new CSV file
	newFileName = sys.argv[1].replace(".csv", "_new.csv")
	with open(newFileName, "w", newline="") as newCsvFile: 
		writer = csv.DictWriter(newCsvFile, fieldnames=header)
		writer.writeheader()
		writer.writerows(newRows)

# print a message indicating the transformation is done and the new filename and show fieldnames that were not in the knownFieldNames list
print("Activities column created! New filename: " + newFileName)
if(len(unknownFieldNames) > 0):
	print("The following fieldnames were not in the knownFieldNames list: " + str(unknownFieldNames))