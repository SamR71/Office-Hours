import requests
import re
import os
import sys
import django
import PyPDF2
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
		#with open("prevSyllabus.PDF", "r") as currentFileReader:
		with open("prevSyllabus.html", "r") as currentFileReader:
			#Read + Obtain All PDF Data:
			currentPDFData = currentFileReader.read()
			currentSoup = BeautifulSoup(currentPDFData, 'html.parser')
			#Find All Subsections For Course Information:
			allSectionValues = currentSoup.find_all("div")
			#Loop Through All Course Descriptions:
			# prevCourseAbbrev = "";
			# allPrevInformation = [];
			countFoundData = 0;
			k = 0;
			while(k < len(allSectionValues)):
				currentSection = allSectionValues[k];
				#Check If Current Section Contains Instructor Information:
				if(currentSection.find_all("p", string=re.compile("Instructor")) != None):
					currentCourseAbbrev = self.computeCourseAbbrevName(allSectionValues, k);
					#Assert Current Section Describes A Valid Section:
					if(currentCourseAbbrev != None):
						print(currentCourseAbbrev)
						allProfessorData, sIndex = self.computeAllProfessorData(allSectionValues, k);
						allProfessorData = self.formatProfessorData(allProfessorData);
						#print(allProfessorData)
						k = sIndex;
						countFoundData += 1;
						print()
				k += 1;
			print(countFoundData);
		
	def computeCourseAbbrevName(self, allSectionValues, sIndex):
		#Find Course Abbreviation:
		currentChildren = allSectionValues[sIndex].findChildren();
		for k in range(0, len(currentChildren)):
			currentInformation = currentChildren[k].get_text().replace('\xa0', ' ');
			isRealCourse, currentAbbrev = self.detectCourseAbbrev(currentInformation);
			if(isRealCourse):
				return currentAbbrev;
		return None;

	def detectCourseAbbrev(self, currentAbbrev):
		#Simply Invalid Input
		if(len(currentAbbrev) < 10):
			return (False, currentAbbrev);
		#Optimization: To Filter Oddly Formatted Course Name Values
		if(len(currentAbbrev) > 10):
			notUsedPortion = currentAbbrev[:-10]
			for currentValue in notUsedPortion:
				if(currentValue.isnumeric()):
					return (False, currentAbbrev)
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

	def computeAllProfessorData(self, allSectionValues, sIndex):
		#Find Start Index of First "Instructor" Information:
		allProfessorData = [];
		startValue = self.getProfessorStartValue(allSectionValues, sIndex);
		currentChildren = allSectionValues[sIndex].findChildren();
		#Current Section Does Not Contains "Instructor" Information:
		if(startValue == None):
			allProfessorDataFound = False;
		#Append Appropriate Values allProfessorData.
		else:
			allProfessorDataFound = self.populateAllProfessorData(startValue, currentChildren, allProfessorData);
		#Try Again If Data Not Found:
		if(not(allProfessorDataFound)):
			#Specifically, Look In Next Section.
			sIndex += 1; 
			#If sIndex Within Bounds:
			if(sIndex < len(allSectionValues)):
				#Get Start of Instructor Data:
				startValue = self.getProfessorStartValue(allSectionValues, sIndex);
				#"Instructor" Was In Previous Section, 
				#...Start Looking From First Piece of Information.
				if(startValue == None):
					startValue = 0;
				#Find Children + Pass To Populate Appropriate Data to allProfessorData
				currentChildren = allSectionValues[sIndex].findChildren();
				allProfessorDataFound = self.populateAllProfessorData(startValue, currentChildren, allProfessorData);
				#Error Check If Not Found In Consecutive Section.
				if(not(allProfessorDataFound)):
					print("Fatal Error In Finding Missing Data In Conseuctive Section.")
					return (None, sIndex);
			else:
				#Could Not Ever Find Data.
				print("Fatal Error In Optimization For Missing Data.");
				return (None, sIndex);
		return (allProfessorData, sIndex);

	def getProfessorStartValue(self, allSectionValues, sIndex):
		#Obtain Start of Keyword "Instructor":
		startValue = None;
		currentChildren = allSectionValues[sIndex].findChildren();
		for k in range(0, len(currentChildren)):
			#Replace '\xa0' with ' '
			currentInformation = currentChildren[k].get_text().replace('\xa0', ' ');
			if("Instructor " == currentInformation):
				startValue = k;
				break;
		return startValue;

	def populateAllProfessorData(self, startValue, currentChildren, allProfessorData):
		#Terminate w/ Keyword "Teaching Assistant(s)":
		for k in range(startValue, len(currentChildren)):
			#Replace '\xa0' with ' '
			currentInformation = currentChildren[k].get_text().replace('\xa0', ' ');
			if("Teaching Assistant(s) " == currentInformation):
				return True;
			else:
				#Populate Professor Data If Non-Empty:
				if(currentInformation != '' and currentInformation != ' '):
					allProfessorData.append(currentInformation);
		#Never Found "Teaching Assistant(s)" => Need To Look In Next Section For Missing Data.
		return False;

	def formatProfessorData(self, allProfessorData):
		#Format Professor Data Prior To Entry Into SQLite3 Database.
		if(allProfessorData == None):
			return None;
		#Remove Trailing ' ' From All Instructor Data.
		for k in range(0, len(allProfessorData)):
			allProfessorData[k] = allProfessorData[k][:-1];
		#Name of Professor:
		pName = allProfessorData[1];
		#Convert Email To @rpi.edu Instead of @RPI.EDU By Converting To Lowecase:
		pEmail = allProfessorData[2].lower();
		#Obtain Professor Office Hour Location:
		pLocation = self.getProfessorLocationValue(allProfessorData[3:]);
		#Obtain Professor Office Hour Data:
		pOfficeHours = self.getProfessorOfficeHours(allProfessorData[3:]);	
		print(pName)
		print(pEmail)
		print(pLocation)
		print(pOfficeHours)
		return allProfessorData;

	def getProfessorLocationValue(self, allProfessorData):
		for k in range(0, len(allProfessorData)):
			if("Office Location: " in allProfessorData[k]):
				return allProfessorData[k][17:];
		return "Currently To Be Determined.";

	def getProfessorOfficeHours(self, allProfessorData):
		#Find Start of Office Hours Data:
		startValue = None;
		currentOfficeHours = [];
		for k in range(0, len(allProfessorData)):
			if("Office Hours: " in allProfessorData[k]):
				startValue = k;
				allProfessorData[k] = allProfessorData[k][14:];
		#Case 1: No Office Data.
		if(startValue == None):
			return [("Not Applicable.","Currently To Be Determined.")];
		#Combine All Office Hours Data Into A Single.
		allDataInSingleStr = "";
		for k in range(startValue, len(allProfessorData)):
			allDataInSingleStr += allProfessorData[k];
			#Do Not Append Space To Very End of Data.
			if(k != len(allProfessorData)-1):
				allDataInSingleStr += " ";
		#Split By Spaces To Extract Date + Time Components.
		tempParserForOfficeHours = allDataInSingleStr.split();
		#Extract Date + Time Components + Populate Into currentOfficeHours.
		for k in range(0, len(tempParserForOfficeHours), 2):
			firstValue = tempParserForOfficeHours[k];
			secondValue = None;
			if(k+1 < len(tempParserForOfficeHours)):
				secondValue = tempParserForOfficeHours[k+1];
			#Case 1: No Date Specified + Just Time
			if(any(currentChar.isdigit() for currentChar in firstValue)):
				secondValue = firstValue;
				firstValue = "Not Specified By Instructor."
				(startTime, endTime) = self.getStartEndTimes(secondValue);
				if(startTime != None and endTime != None):
					currentOfficeHours.append((firstValue, startTime, endTime))
				k -= 1;
			#Case 2: Date Specified
			else:
				#Case 3: Time Specified
				if(secondValue != None):
					(startTime, endTime) = self.getStartEndTimes(secondValue);
					if(startTime != None and endTime != None):
						currentOfficeHours.append((firstValue, startTime, endTime))
		#No Correct Office Hours Data Found:
		if(len(currentOfficeHours) == 0):
			return [("Not Applicable.","Currently To Be Determined.")];
		return currentOfficeHours;

	def getStartEndTimes(self, currentCombinedTime):
		for k in range(0, len(currentCombinedTime)):
			if(currentCombinedTime[k] == "-"):
				#Compute Start + End Time + Return Pair of Them
				return (currentCombinedTime[:k], currentCombinedTime[k+1:]);
		return (None, None);

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



