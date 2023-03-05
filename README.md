# XMLTools
Some useful Python scripts for specific use cases in XML processing. This repository was created as part of a final year university project, therefore it is not guaranteed to be bug-free or to work in all cases, it has only been tested for the specific use case it was created for.  
These scripts were created to automate processing of some XML files that were generated within ServiceNow instance. Ultimate goal is to transform the data as required and then import it into a process mining tool platform - Celonis for further analysis.  
## split.py
This script takes a **filename as a parameter**. 
The script contains some hardcoded values that determine how to split the file. It will split the digested files into two files - `output_incident.xml` and `output_audit.xml`.  
It loops through all the tags in the root of the digested file and based on the tag name, it will write the tag to the appropriate file.  
- Tags `<incident>` (and all nested tags within) will be written to `output_incident.xml`  
- Tags `<audit>` (and all nested tags within) will be written to `output_audit.xml`.
The following digest file structure is assumed:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<root>
	<incident>
		<field1>value1</field1>
		<field2>value2</field2>
	</incident>
	<incident>
		<field1>value1</field1>
		<field2>value2</field2>
	</incident>
	<audit>
		<field1>value1</field1>
		<field2>value2</field2>
	</audit>
	<audit>
		<field1>value1</field1>
		<field2>value2</field2>
	</audit>
</root>
```
Output files will have the following structure:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<group split_date="1970-01-01 00:00:00">
	<incident>
		<field1>value1</field1>
		<field2>value2</field2>
	</incident>
	<incident>
		<field1>value1</field1>
		<field2>value2</field2>
	</incident>
</group>
```
AND
```xml
<?xml version="1.0" encoding="UTF-8"?>
<group split_date="1970-01-01 00:00:00">
	<audit>
		<field1>value1</field1>
		<field2>value2</field2>
	</audit>
	<audit>
		<field1>value1</field1>
		<field2>value2</field2>
	</audit>
</group>
```
## cleanUsers.py
This is a very similar script to `split.py`.  
Again, takes a **filename as a parameter** and then it has some hardcoded values that determine which tags to keep and which to remove. Everything that should be kept for further processing is written to `output_user.xml`. 
Tags that are kept are:
- `<x_qdsdp_bnp_candidate>` (and all nested tags within)
- `<sys_user>` (and all nested tags within)
## makeCSV.py
This is a more flexible script that can be used to convert any XML file to a CSV file.  
It again takes a single parameter - name of the XML file to be converted. Output contents will be written to a file that has the same name as the input file, but with a `.csv` extension.  
Example: `convert.xml` will be converted to `convert.csv`.  
The script is designed to extract data from subchild records **AS WELL AS their attributes**. 
Thought was also given to the fact that attributes can change from record to record. Therefore, the script will extract **all attributes from all records** and create a column for each attribute, unlike some other scripts that only extract structure from the first record occured.  
Therefore, to extract data properly, the following XML structure is assumed:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<root>
	<record>
		<field1 attribute="att_val">value1</field1>
		<field2>value2</field2>
	</record>
	<record>
		<field1 different_attribute="att_val2">value1</field1>
		<field2>value2</field2>
	</record>
	<record>
		<field1>value1</field1>
		<field2>value2</field2>
	</record>
</root>
```
The script will extract the following data:
```csv
field1,field1/attribute,field1/different_attribute,field2
value1,att_val,,value2
value1,,att_val2,value2
value1,,value2
```
For simplicity, this is the output in a table format:
| field1 | field1/attribute | field1/different_attribute | field2 |
| --- | --- | --- | --- |
| value1 | att_val | | value2 |
| value1 | | att_val2 | value2 |
| value1 | | | value2 |
## amendCSV.py
This script takes a single parameter - name of the CSV file to be amended.  
Output contents will be written to a file that has the same name as the input file, but with a `_new.csv` extension.
Example: `convert.csv` will be amended to `convert_new.csv`.
At the moment, its function is to move the `sys_id` to be the first one. 