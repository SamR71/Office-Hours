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
			#Loop Through All Course Descriptions:
			prevCourseAbbrev = "";
			allPrevInformation = [];
			foundCourse = True;
			for currentSection in allSectionValues:
				#Check If Current Section Contains Instructor Information:
				if(currentSection.find_all("p", string=re.compile("Instructor")) != None):
					currentChildren = currentSection.findChildren();
					#Find Start Index of First "Instructor" Information:
					startValue = None;
					for k in range(0, len(currentChildren)):
						if("Instructor" in str(currentChildren[k])):
							startValue = k;
							break;
					computeI = False;
					computeT = False;
					allProfessorData = [];
					allTAData = [];
					singleTAData = [];
					#Case 1: Current Section Contains "Instructor" Information:
					if(startValue != None):
						computeI = True;
					#Case 2: No "Instructor" Information
					else:
						startValue = len(currentChildren);
						#Special Case:
						#We May Have Already Seen "Instructor" In Previous Section.
						#But Not The Interesting Data.
						if(not(foundCourse)):
							startValue = 0;
							computeI = True;
							#Initialize Data For Professor.
							allProfessorData = allPrevInformation;
					#Append Appropriate Values allProfessorData/allTAData.
					for k in range(startValue, len(currentChildren)):
						#Termination Condition For Professor Data.	
						#Start Condition For TA Data.
						if("Teaching" in str(currentChildren[k])):	
							computeI = False;
							computeT = True;
							singleTAData = [];
						#Termination Condition For A Single TA Information.
						if(computeI == False and computeT == True and "@rpi.edu" in str(currentChildren[k])):
							singleTAData.append(currentChildren[k])
							allTAData.append(singleTAData);
							singleTAData = [];
						else:
							#Append Professor Data.
							if(computeI):
								allProfessorData.append(currentChildren[k]);
							#Append TA Data.
							if(computeT):
								singleTAData.append(currentChildren[k]);

					#Optimization: Account For Data Spread Across Multiple Sections.
					if(not(foundCourse)):
						prevCourseAbbrev = self.formatCourseAbbrevWithoutHypen(prevCourseAbbrev)
						isCourseValue, currentAbbrev = self.detectCourseAbbrev(prevCourseAbbrev);
						if(isCourseValue):
							#Append Professor Office Hours Now:
							if(self.appendProfessorOfficeHours(currentAbbrev, allProfessorData, allPrevInformation)):
								foundCourse = True;
								allPrevInformation = [];
							#Append TA Office Hours Now:
							self.appendTAOfficeHours(allTAData);
					else:		
						#Find Course Abbreviation:
						for k in range(0, len(currentChildren)):
							if(currentChildren[k] != None):
								currentLineString = currentChildren[k].get_text()
								isCourseValue, currentAbbrev = self.detectCourseAbbrev(currentLineString);
								if(isCourseValue):
									#Append Professor Office Hours Now:
									if(not(self.appendProfessorOfficeHours(currentAbbrev, allProfessorData, allPrevInformation))):
										prevCourseAbbrev = currentAbbrev;
										foundCourse = False;
									else:
										foundCourse = True;
										allPrevInformation = [];
									#Append TA Office Hours Now:
									self.appendTAOfficeHours(allTAData);
					
					
	def detectCourseAbbrev(self, currentAbbrev):
		#Simply Invalid Input
		if(len(currentAbbrev) < 10):
			return (False, currentAbbrev);
		#Optimization: To Filter Oddly Formatted Course Name Values
		if(len(currentAbbrev) > 10):
			currentAbbrev = currentAbbrev[-10:]
		#Sanity Check After Setting currentAbbrev To Only 10 Characters.
		if(len(currentAbbrev) != 10):
			return (False, currentAbbrev);
		#Check For Four Alpha Characters:
		for k in range(0, 4):
			if(not(currentAbbrev[k].isalpha() and currentAbbrev[k].isupper())):
				return (False, currentAbbrev);
		#Check For Middle Space:
		if(not(currentAbbrev[4].isspace())):
			return (False, currentAbbrev);
		#Check For Four Digits:
		for k in range(5, 9):
			if(not(currentAbbrev[k].isnumeric())):
				return (False, currentAbbrev);
		#Check For Last Space:
		if(not(currentAbbrev[9].isspace())):
			return (False, currentAbbrev);
		currentAbbrev = self.formatCourseAbbrevWithHypen(currentAbbrev);
		#Case That We Do Not Have Course From Spring 2019 Now, Then Disregard. 
		allExistingCourses = Course.objects.filter(courseAbbrev = currentAbbrev);
		returnValue = (len(allExistingCourses) != 0)
		return (returnValue, currentAbbrev);

	def formatCourseAbbrevWithHypen(self, currentAbbrev):
		#Append Hypen To Existing Abbrev + Remove Last Space Character
		return currentAbbrev[:4] + "-" + currentAbbrev[5:9];

	def formatCourseAbbrevWithoutHypen(self, currentAbbrev):
		#Remove Hypen From Existing Abbrev + Append Last Space Character
		return currentAbbrev[:4] + " " + currentAbbrev[5:9] + " ";

	def appendProfessorOfficeHours(self, currentAbbrev, allProfessorData, allPrevInformation):
		#Email Data:
		currentEmail = "";
		currentEmailHTML = None;
		#OH Data:
		computeOfficeHours = False;
		currentOfficeHours = [];
		for k in range(0, len(allProfessorData)):
			#Case 1: Email.
			if("rpi.edu" in str(allProfessorData[k]) or "RPI.EDU" in str(allProfessorData[k]) or "@" in str(allProfessorData[k])):
				currentEmail = allProfessorData[k].get_text().replace('\xa0','')
				currentEmailHTML = allProfessorData[k];
			#Case 2: First Instance of Office Hours.
			if("Office" in str(allProfessorData[k]) and not("Location") in str(allProfessorData[k])):
				noLower = True;
				#Set computeOfficeHours Flag To True For Next Iteration.
				computeOfficeHours = True;
				currentOH = allProfessorData[k].get_text().replace('\xa0', ' ')
				currentOH = currentOH.strip("Office ").strip("Hours:")
				#Check For Invalid Data:
				for currentChar in currentOH:
					if(currentChar.isalpha() and currentChar.islower()):
						noLower = False;
				#Append Valid + Non-Empty Data
				if(len(currentOH) != 0 and noLower):
					currentOfficeHours.append(currentOH)
			#Case 3: All Other Instances of Office Hours:
			elif(computeOfficeHours):
				noLower = True
				currentOH = allProfessorData[k].get_text().replace('\xa0', ' ')
				currentOH = currentOH.strip("Office ").strip("Hours:")
				#Check For Invalid Data:
				for currentChar in currentOH:
					if(currentChar.isalpha() and currentChar.islower()):
						noLower = False;
				#Append Valid + Non-Empty Data
				if(len(currentOH) != 0 and noLower):
					currentOfficeHours.append(currentOH)
		if(len(currentOfficeHours) == 0):
			if(currentEmail != ""):
				allPrevInformation.append(currentEmailHTML);
			return False
		print(currentAbbrev, currentEmail, currentOfficeHours)
		#self.populateProfessorData(currentAbbrev, currentEmail, currentOfficeHours)
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

