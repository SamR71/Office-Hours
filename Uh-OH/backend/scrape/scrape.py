import requests
import re
from bs4 import BeautifulSoup

currentPageData = requests.get("https://sis.rpi.edu/reg/zs202001.htm");
currentSoup = BeautifulSoup(currentPageData.text, "lxml");

allCourseData = [];
allTableLocations = currentSoup.find_all('table');
for currentTable in allTableLocations:
	#Find New Row:
	allTableRows = currentTable.find_all('tr');
	for currentRow in allTableRows:
		#Read Each Column Value From Row:
	    allTableColumns = currentRow.find_all('td');
	    allTableColumns = [currentColumn.text.strip() for currentColumn in allTableColumns]
	    currentData = [currentColumn for currentColumn in allTableColumns];

	    if(len(currentData) != 0):
	    	#print(len(currentData));
	    	currentData = currentData[0];
	    	if(currentData != ""):
	    		allCourseData.append(currentData);
for currentCourse in allCourseData:
	print(currentCourse)
print(len(allCourseData))

#Not Used Beautiful Soup Code:
# def my_filter(tag):
#     if(tag.name == 'span' and "Course Title" in tag.text):
#     	return True;
#     return False;

# currentPageData = requests.get("https://sis.rpi.edu/reg/zs202001.htm");
# currentSoup = BeautifulSoup(currentPageData.text, "html.parser");
# allCourseValues = [];
# allTitleValues = currentSoup.find_all(my_filter);
# print(len(allTitleValues))

# for currentTitle in allTitleValues:
# 	#print(currentTitle.children)
# 	for child in currentTitle.children:
# 		print(child)
# 	#allCurrentChildren = currentTitle.
# 	#print(allCurrentChildren)
