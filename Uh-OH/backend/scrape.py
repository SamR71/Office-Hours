import requests
import re
from bs4 import BeautifulSoup

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
import django
django.setup()

from scrape.models import Course, CourseSection

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
	    	if(currentData[1] != "" and len(currentData) == 14):
	    		if(currentData[1] == "MULTIVAR CALC & MATRIX ALG"):
	    			currentData[1] = "MULTIVAR CALC & MATRIX ALGEBRA";
	    		allCourseData.append(currentData);

currentDataInDatabase = Course.objects.all();
if(len(currentDataInDatabase) != 0):
	#print(currentDataInDatabase)
	currentDataInDatabase.delete();

for currentCourse in allCourseData:
	currentNewCourse = Course.objects.filter(courseName = currentCourse[1]);
	if(len(currentNewCourse) == 0):
		currentNewCourse = Course(courseName = currentCourse[1]);
		currentNewCourse.save();
		currentSection = CourseSection(course = currentNewCourse, 
										sectionID = currentCourse[0][-2:],
										instructorName = currentCourse[8]);
		currentSection.save();
	else:
		currentNewCourse = currentNewCourse[0];
		currentSection = CourseSection(course = currentNewCourse, 
										sectionID = currentCourse[0][-2:],
										instructorName = currentCourse[8]);
		currentSection.save();
	#print(currentCourse[1])
#print(len(allCourseData))

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
