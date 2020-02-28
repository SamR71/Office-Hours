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
		currentPageData = requests.get("https://sis.rpi.edu/reg/zs202001.htm")
		currentSoup = BeautifulSoup(currentPageData.text, "lxml")

		prevCourseData = None
		allCourseData = []
		allTableLocations = currentSoup.find_all('table')
		for currentTable in allTableLocations:
			#Find New Row:
			allTableRows = currentTable.find_all('tr')
			for currentRow in allTableRows:
				#Read Each Column Value From Row:
			    allTableColumns = currentRow.find_all('td')
			    allTableColumns = [currentColumn.text.strip() for currentColumn in allTableColumns]
			    currentData = [currentColumn for currentColumn in allTableColumns]

			    if(len(currentData) != 0):
			    	if(len(currentData) == 14):
				    	if(currentData[1] != ""):
				    		#Special Case Accounting For Error In Website Format:
					    	if(currentData[1] == "MULTIVAR CALC & MATRIX ALG"):
					    		currentData[1] = "MULTIVAR CALC & MATRIX ALGEBRA"
					    	prevCourseData = currentData
				    	else:
				    		if(prevCourseData != None):
				    			currentData[0] = prevCourseData[0]
				    			currentData[1] = prevCourseData[1]
				    	allCourseData.append(currentData)

		#Clear Database Prior To Population:
		currentDataInDatabase = Course.objects.all()
		if(len(currentDataInDatabase) != 0):
			currentDataInDatabase.delete()

		#Populate All Spring 2020 Course Data:
		for currentRow in allCourseData:
			allExistingCourses = Course.objects.filter(courseName = currentRow[1])
			if(len(allExistingCourses) == 0):
				currentName = currentRow[1]
				currentValue, currentAbbrev = currentRow[0][0:5], currentRow[0][6:15]
				currentNewCourse = Course(courseName = currentName, 
												courseValue = currentValue,
												courseAbbrev = currentAbbrev)
				currentNewCourse.save()
				currentSection = CourseSection(currentCourse = currentNewCourse, 
												sectionID = currentRow[0][-2:])
				currentSection.save()
				currentMeeting = CourseMeetingTime(meetSection = currentSection,
												meetType = currentRow[2],
												meetDates = currentRow[5].replace(" ", ""),
												meetStartTime = currentRow[6],
												meetEndTime = currentRow[7],
												meetInstructor = currentRow[8])
				currentMeeting.save()
			else:
				allExistingSections = CourseSection.objects.filter(currentCourse = allExistingCourses[0]).filter(sectionID = currentRow[0][-2:])
				if(len(allExistingSections) == 0):
					currentSection = CourseSection(currentCourse = allExistingCourses[0], 
													sectionID = currentRow[0][-2:])	
					currentSection.save()
					currentMeeting = CourseMeetingTime(meetSection = currentSection,
												meetType = currentRow[2],
												meetDates = currentRow[5],
												meetStartTime = currentRow[6],
												meetEndTime = currentRow[7],
												meetInstructor = currentRow[8])
					currentMeeting.save()
				else:
					currentMeeting = CourseMeetingTime(meetSection = allExistingSections[0],
												meetType = currentRow[2],
												meetDates = currentRow[5].replace(" ", ""),
												meetStartTime = currentRow[6],
												meetEndTime = currentRow[7],
												meetInstructor = currentRow[8])
					currentMeeting.save()
	#Scrape All Spring 2019 Office Hours:
	def scrapeSpring2019OfficeHours(self):
		#Reset Database Values Prior To Population:
		# currentProfessorDataInDatabase = Professor.objects.all()
		# if(len(currentProfessorDataInDatabase) != 0):
		# 	currentProfessorDataInDatabase.delete()
		# currentTADataInDatabase = TeachingAssistant.objects.all()
		# if(len(currentTADataInDatabase) != 0):
		# 	currentTADataInDatabase.delete()
		#Begin Scrape Procedure:
		with open("prevSyllabus.html", "r") as currentFileReader:
			currentPDFData = currentFileReader.read()
			currentSoup = BeautifulSoup(currentPDFData, 'html.parser')
			#Find All Subsections For Course Information:
			allSectionValues = currentSoup.find_all("div")
			print(len(allSectionValues))
			#Loop Through All Course Descriptions:
			count = 0;
			prevCourseAbbrev = "";
			foundCourse = True;
			for currentSection in allSectionValues:
				#Check If Current Section Contains Instructor Information:
				if(currentSection.find_all("p", string=re.compile("Instructor")) != None):
					currentChildren = currentSection.findChildren();

					#Find Start Index of "Instructor" Information:
					startValue = None;
					for k in range(0, len(currentChildren)):
						if("Instructor" in str(currentChildren[k])):
							startValue = k;
					
					#Obtain Only Instructor Information:
					computeI = False;
					if(startValue != None):
						computeI = True;
					else:
						startValue = 0;
					computeT = False;
					allProfessorData = [];
					allTAData = [];
					singleTAData = [];
					for k in range(startValue, len(currentChildren)):
						if("Teaching" in str(currentChildren[k])):	
							computeI = False;
							computeT = True;
							singleTAData = [];
						if(computeI == False and computeT == True and "@rpi.edu" in str(currentChildren[k])):
							singleTAData.append(currentChildren[k])
							allTAData.append(singleTAData);
							singleTAData = [];
						else:
							if(computeI):
								allProfessorData.append(currentChildren[k]);
							if(computeT):
								singleTAData.append(currentChildren[k]);

					#Account For The Format of Instructor Information:
					#That is, if invalid, continue.
					#Example: Random Course Information Text That Contains 
					#The Word "Instructor" ...
					#print(currentSection)

					if(not(foundCourse)):
						prevCourseAbbrev = self.formatCourseAbbrevWithoutHypen(prevCourseAbbrev)
						isCourseValue, currentAbbrev = self.detectCourseAbbrev(prevCourseAbbrev);
						if(isCourseValue):
							print(currentAbbrev)
							count += 1;
							#Append Professor Office Hours Now:
							if(self.appendProfessorOfficeHours(allProfessorData)):
								foundCourse = True;
							#Append TA Office Hours Now:
							self.appendTAOfficeHours(allTAData);
					else:		
						for k in range(0, len(currentChildren)):
							if(currentChildren[k] != None):
								currentLineString = currentChildren[k].get_text()
								if(currentLineString != None):
									isCourseValue, currentAbbrev = self.detectCourseAbbrev(currentLineString);
									if(isCourseValue):
										print(currentAbbrev)
										count += 1;
										#Append Professor Office Hours Now:
										if(not(self.appendProfessorOfficeHours(allProfessorData))):
											prevCourseAbbrev = currentAbbrev;
											foundCourse = False;
											break;
										#Append TA Office Hours Now:
										self.appendTAOfficeHours(allTAData);
					
			print(count)

	def detectCourseAbbrev(self, currentAbbrev):
		if(len(currentAbbrev) < 10):
			return (False, currentAbbrev);
		#Optimization To Filter Oddly Formatted Course Name Values
		if(len(currentAbbrev) > 10):
			currentAbbrev = currentAbbrev[-10:]
		if(len(currentAbbrev) != 10):
			return (False, currentAbbrev);
		for k in range(0, 4):
			if(not(currentAbbrev[k].isalpha() and currentAbbrev[k].isupper())):
				return (False, currentAbbrev);
		if(not(currentAbbrev[4].isspace())):
			return (False, currentAbbrev);
		for k in range(5, 9):
			if(not(currentAbbrev[k].isnumeric())):
				return (False, currentAbbrev);
		if(not(currentAbbrev[9].isspace())):
			return (False, currentAbbrev);
		currentAbbrev = self.formatCourseAbbrevWithHypen(currentAbbrev);
		#Case That We Do Not Have Course From Spring 2019 Now, Then Disregard. 
		allExistingCourses = Course.objects.filter(courseAbbrev = currentAbbrev);
		returnValue = (len(allExistingCourses) != 0)
		return (returnValue, currentAbbrev);

	def formatCourseAbbrevWithHypen(self, currentAbbrev):
		return currentAbbrev[:4] + "-" + currentAbbrev[5:9];

	def formatCourseAbbrevWithoutHypen(self, currentAbbrev):
		return currentAbbrev[:4] + " " + currentAbbrev[5:9] + " ";

	def appendProfessorOfficeHours(self, allProfessorData):
		computeOfficeHours = False;
		currentEmail = "";
		currentOfficeHours = [];
		for k in range(0, len(allProfessorData)):
			print(allProfessorData[k])
			if("@rpi.edu" in str(allProfessorData[k])):
				currentEmail = allProfessorData[k].get_text().replace('\xa0','')
			if("Office" in str(allProfessorData[k]) and not("Location") in str(allProfessorData[k])):
				computeOfficeHours = True;
				currentOH = allProfessorData[k].get_text().replace('\xa0', '')
				currentOH = currentOH.strip("Office ").strip("Hours:")
				noLower = True;
				for currentChar in currentOH:
					if(currentChar.isalpha() and currentChar.islower()):
						noLower = False;
				if(len(currentOH) != 0 and noLower):
					currentOfficeHours.append(currentOH)
			elif(computeOfficeHours):
				currentOH = allProfessorData[k].get_text().replace('\xa0', '')
				currentOH = currentOH.strip("Office ").strip("Hours:")
				noLower = True
				for currentChar in currentOH:
					if(currentChar.isalpha() and currentChar.islower()):
						noLower = False;
				if(len(currentOH) != 0 and noLower):
					currentOfficeHours.append(currentOH)
		print(currentOfficeHours)
		if(len(currentOfficeHours) == 0):
			return False
		return True

	def appendTAOfficeHours(self, allTAData):
		return;

def main():
    if(len(sys.argv) < 2):
    	print("Incorrect Number of Arguments.")
    	return
    else:
    	scrapeValue = int(sys.argv[1])
    	currentScrape = Scrape()
    	if(scrapeValue == 0):
    		print("Start of Scrape Spring 2020 Course Data.")
    		currentScrape.scrapeSpring2020Courses()
    		print("Termination of Scrape Spring 2020 Course Data.")
    	else:
    		print("Start of Scrape Spring 2019 Office Hours Data.")
    		currentScrape.scrapeSpring2019OfficeHours()
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
#     	return True
#     return False

# currentPageData = requests.get("https://sis.rpi.edu/reg/zs202001.htm")
# currentSoup = BeautifulSoup(currentPageData.text, "html.parser")
# allCourseValues = []
# allTitleValues = currentSoup.find_all(my_filter)
# print(len(allTitleValues))

# for currentTitle in allTitleValues:
# 	#print(currentTitle.children)
# 	for child in currentTitle.children:
# 		print(child)
# 	#allCurrentChildren = currentTitle.
# 	#print(allCurrentChildren)

