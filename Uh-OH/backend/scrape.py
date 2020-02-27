import requests
import re
import os
import sys
import django
from bs4 import BeautifulSoup
#Necessary Setup To Import Models:
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
from scrape.models import Course, CourseSection, CourseMeetingTime

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
		for currentRow in allCourseData:
			allExistingCourses = Course.objects.filter(courseName = currentRow[1]);
			if(len(allExistingCourses) == 0):
				currentName = currentRow[1];
				currentValue, currentAbbrev = currentRow[0][0:5], currentRow[0][6:15];
				currentNewCourse = Course(courseName = currentName, 
												courseValue = currentValue,
												courseAbbrev = currentAbbrev);
				currentNewCourse.save();
				currentSection = CourseSection(currentCourse = currentNewCourse, 
												sectionID = currentRow[0][-2:]);
				currentSection.save();
				currentMeeting = CourseMeetingTime(meetSection = currentSection,
												meetType = currentRow[2],
												meetDates = currentRow[5].replace(" ", ""),
												meetStartTime = currentRow[6],
												meetEndTime = currentRow[7],
												meetInstructor = currentRow[8]);
				currentMeeting.save();
			else:
				allExistingSections = CourseSection.objects.filter(currentCourse = allExistingCourses[0]).filter(sectionID = currentRow[0][-2:]);
				if(len(allExistingSections) == 0):
					currentSection = CourseSection(currentCourse = allExistingCourses[0], 
													sectionID = currentRow[0][-2:]);	
					currentSection.save();
					currentMeeting = CourseMeetingTime(meetSection = currentSection,
												meetType = currentRow[2],
												meetDates = currentRow[5],
												meetStartTime = currentRow[6],
												meetEndTime = currentRow[7],
												meetInstructor = currentRow[8]);
					currentMeeting.save();
				else:
					currentMeeting = CourseMeetingTime(meetSection = allExistingSections[0],
												meetType = currentRow[2],
												meetDates = currentRow[5].replace(" ", ""),
												meetStartTime = currentRow[6],
												meetEndTime = currentRow[7],
												meetInstructor = currentRow[8]);
					currentMeeting.save();
	#Scrape All Spring 2019 Office Hours:

	def my_filter(self, tag):
		if("Office" in tag.text):
			return True;
		return False;
			

	def scrapeSpring2019OfficeHours(self):
		with open("prevSyllabus.html", "r") as currentFileReader:
			currentPDFData = currentFileReader.read()
			currentSoup = BeautifulSoup(currentPDFData, "html.parser")
			for child in currentSoup.recursiveChildGenerator():
				if child.name:
					print(child.name)

def main():
    if(len(sys.argv) < 2):
    	print("Incorrect Number of Arguments.");
    	return;
    else:
    	scrapeValue = int(sys.argv[1]);
    	currentScrape = Scrape();
    	if(scrapeValue == 0):
    		print("Start of Scrape Spring 2020 Course Data.")
    		currentScrape.scrapeSpring2020Courses();
    		print("Termination of Scrape Spring 2020 Course Data.")
    	else:
    		print("Start of Scrape Spring 2019 Office Hours Data.")
    		currentScrape.scrapeSpring2019OfficeHours();
    		print("Termination of Scrape Spring 2019 Office Hours Data.")
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

