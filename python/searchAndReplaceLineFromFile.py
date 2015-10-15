import fileinput
import sys

#function for search a line and replace it with new line
def replaceAll(file,searchExp,replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

# to search line starting with root 
oldString=''
newLine=''
oldLine=''
filePath="/etc/passwd"
with open(filePath, 'r') as f:
	lines = f.readlines()
    	for str in lines:
        	if str.startswith("root"):
            		oldLine=str
			#split the line to get the shell of that user
	    		strArr=str.split(":")
            		oldString=strArr[6]
			newLine=str.replace(oldString, "/bin/bash\n")

replaceAll(filePath,oldLine, newLine)
