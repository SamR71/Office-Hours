import requests
import re
import os
import sys
import django
from bs4 import BeautifulSoup
#Necessary Setup To Import Models:
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
from scrape.models import Course, CourseSection

#Scrape Class For All Formats:
class Scrape(object):

	#Scrape All Spring 2020 Courses:
	def scrapeSpring2020Courses(self):
		currentPageData = requests.get("https://sis.rpi.edu/reg/zs202001.htm");
		currentSoup = BeautifulSoup(currentPageData.text, "lxml");

		prevCourseData = None;
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
			    	if(len(currentData) == 14):
				    	if(currentData[1] != ""):
				    		#Special Case Accounting For Error In Website Format:
					    	if(currentData[1] == "MULTIVAR CALC & MATRIX ALG"):
					    		currentData[1] = "MULTIVAR CALC & MATRIX ALGEBRA";
					    	prevCourseData = currentData;
				    	else:
				    		if(prevCourseData != None):
				    			currentData[0] = prevCourseData[0]
				    			currentData[1] = prevCourseData[1]
				    	allCourseData.append(currentData);

		#Clear Database Prior To Population:
		currentDataInDatabase = Course.objects.all();
		if(len(currentDataInDatabase) != 0):
			currentDataInDatabase.delete();

		#Populate All Spring 2020 Course Data:
		for currentCourse in allCourseData:
			currentNewCourse = Course.objects.filter(courseName = currentCourse[1]);
			if(len(currentNewCourse) == 0):
				currentName = currentCourse[1];
				currentValue, currentAbbrev = currentCourse[0][0:5], currentCourse[0][6:15];
				currentNewCourse = Course(courseName = currentName, 
												courseValue = currentValue,
												courseAbbrev = currentAbbrev);
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

def main():
    if(len(sys.argv) < 2):
    	print("Incorrect Number of Arguments.");
    	return;
    else:
    	scrapeValue = int(sys.argv[1]);
    	if(scrapeValue == 0):
    		print("Start of Scrape Spring 2020 Course Data.")
    		currentScrape = Scrape();
    		currentScrape.scrapeSpring2020Courses();
    		print("Termination of Scrape Spring 2020 Course Data.")

if __name__ == "__main__":
    main()

#Unused Possibly Useful Code:
#Should Probably Delete.
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
