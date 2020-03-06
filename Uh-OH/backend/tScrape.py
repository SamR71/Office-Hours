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
from scrape.models import Course, CourseSection, CourseMeetingTime, Professor, ProfessorOfficeHours

#---------------------------------------------------------------------------------------------------

#This Class Is Used To Parse All Course + Course-Related Information 
#From The Spring 2020 SIS Public Website. 
class ParseForCourse(object):
	#Constructor:
	#Stores self.allCourseData 
	#So That Client Can Access After computeAllCourseData().
	def __init__(self):
		self.allCourseData = [];
		self.currentPageData = requests.get("https://sis.rpi.edu/reg/zs202001.htm")
		self.currentSoup = BeautifulSoup(self.currentPageData.text, "lxml")

	#Public Function:
	#Determines All Course Course Data Present In Current SIS Public Webpage.
	#Specific To Format of curentSoup;
	def computeAllCourseData(self):
		prevCourseData = None
		allTableLocations = self.currentSoup.find_all('table')
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
				    	self.allCourseData.append(currentData)

#---------------------------------------------------------------------------------------------------

#This Class Is Used To Populate 
#The Current Course + Course Section + Meeting Time
#Data Into Our Backend Django SQLite3 Database.
class PopulateForCourse(object):
	#Constructor: 
	#Stores self.allCourseData To Be Placed Into Database.
	def __init__(self, currentCourseData):
		self.allCourseData = currentCourseData;

	#Public Function:
	#Runs Population of self.allCourseData Into Database.
	def runPopulateCourseData(self):
		for currentRow in self.allCourseData:
			allExistingCourses = Course.objects.filter(courseName = currentRow[1])
			#New Unseen Course:
			if(len(allExistingCourses) == 0):
				currentName = currentRow[1]
				currentValue, currentAbbrev = currentRow[0][0:5], currentRow[0][6:15]
				#Create New Course:
				currentNewCourse = Course(courseName = currentName, 
												courseValue = currentValue,
												courseAbbrev = currentAbbrev)
				currentNewCourse.save()
				#Current New Section:
				currentSection = CourseSection(currentCourse = currentNewCourse, 
												sectionID = currentRow[0][-2:])
				currentSection.save()
				#Create New Meeting Time:
				currentMeeting = CourseMeetingTime(meetSection = currentSection,
												meetType = currentRow[2],
												meetDates = currentRow[5].replace(" ", ""),
												meetStartTime = currentRow[6],
												meetEndTime = currentRow[7],
												meetInstructor = currentRow[8])
				currentMeeting.save()
			else:
				#Find Existing Course Section:
				allExistingSections = CourseSection.objects.filter(currentCourse = allExistingCourses[0]).filter(sectionID = currentRow[0][-2:])
				if(len(allExistingSections) == 0):
					#Create New Course Section:
					currentSection = CourseSection(currentCourse = allExistingCourses[0], 
													sectionID = currentRow[0][-2:])	
					currentSection.save()
					#Create New Meeting Time:
					currentMeeting = CourseMeetingTime(meetSection = currentSection,
												meetType = currentRow[2],
												meetDates = currentRow[5],
												meetStartTime = currentRow[6],
												meetEndTime = currentRow[7],
												meetInstructor = currentRow[8])
					currentMeeting.save()
				else:
					#Create New Meeting Time Based On Prior Existing Course Section:
					currentMeeting = CourseMeetingTime(meetSection = allExistingSections[0],
												meetType = currentRow[2],
												meetDates = currentRow[5].replace(" ", ""),
												meetStartTime = currentRow[6],
												meetEndTime = currentRow[7],
												meetInstructor = currentRow[8])
					currentMeeting.save()

#---------------------------------------------------------------------------------------------------					

#This Function Will Used By Both ParseForProfessor, ParseForTA Classes.
#Specifically, getStartEndTimes Provides The Formatted Start/End Times
#For A Particular Office Hours String, currentCombinedTime.
def getStartEndTimes(currentCombinedTime):
	for k in range(0, len(currentCombinedTime)):
		if(currentCombinedTime[k] == "-"):
			#Compute Start + End Time + Return Pair of Them
			return (currentCombinedTime[:k], currentCombinedTime[k+1:]);
	return (None, None);

#---------------------------------------------------------------------------------------------------

#This Class Is Used To Compute The Current Course Abbreviation 
#From A Particular Section of the Spring 2019 Syllabus PDF. 
class ParseForCourseAbbrev(object):

	#Constructor:
	#Only Holds Identity/Course Abbreviation.
	#Client Acesses currentIdentityValue After Invoking computeCourseAbbrevName().
	def __init__(self):
		self.currentIdentityValue = None;

	#Public Function:
	#Determines The Course Abbreviation.
	#Return True If Current Section Describes Course Currently Present
	#In Database.
	#Else, Returns False.
	def computeCourseAbbrevName(self, allSectionValues, sIndex):
		#Find Course Abbreviation:
		currentChildren = allSectionValues[sIndex].findChildren();
		for k in range(0, len(currentChildren)):
			currentInformation = currentChildren[k].get_text().replace('\xa0', ' ');
			isRealCourse, currentAbbrev = self.__detectCourseAbbrev(currentInformation);
			if(isRealCourse):
				self.currentIdentityValue = currentAbbrev;

	#Private Function:
	#Detects If Current Line = Valid Course Abbreviation.
	#Checks Current Line = Course Present In Database. 
	def __detectCourseAbbrev(self, currentAbbrev):
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
		currentAbbrev = self.__formatCourseAbbrevWithHypen(currentAbbrev);
		#Case That We Do Not Have Course From Spring 2019 Now, Then Disregard. 
		allExistingCourses = Course.objects.filter(courseAbbrev = currentAbbrev);
		returnValue = (len(allExistingCourses) != 0)
		return (returnValue, currentAbbrev);

	#Private Function:
	#Called To Reformat Current Line.
	#Invoked Prior To Checking If Specified-Course Present In Database.
	#Needed b/c Course Abbreviations In Database Are Specifically w/ "-".
	def __formatCourseAbbrevWithHypen(self, currentAbbrev):
		#Append Hypen To Existing Abbrev + Remove Last Space Character
		return currentAbbrev[:4] + "-" + currentAbbrev[5:9];

#---------------------------------------------------------------------------------------------------

#This Class Is Used To Parse The Current Professor Data + Office Hours 
#From A Particular Section/Course Of The Spring 2019 Syllabus PDF. 		
class ParseForProfessor(object):
	
	#Constructor:
	#Client Will Access self.allProfessorData After Invoking computeAllProfessorData().
	def __init__(self):
		self.allProfessorData = [];

	#Public Function:
	#Calculates Correct Data For Professor Specified By Current Section of PDF.
	def computeAllProfessorData(self, allSectionValues, sIndex):
		#Find Start Index of First "Instructor" Information:
		startValue = self.__getProfessorStartValue(allSectionValues, sIndex);
		currentChildren = allSectionValues[sIndex].findChildren();
		#Current Section Does Not Contains "Instructor" Information:
		if(startValue == None):
			allProfessorDataFound = False;
		#Append Appropriate Values allProfessorData.
		else:
			allProfessorDataFound = self.__putAllProfessorData(startValue, currentChildren);
		#Try Again If Data Not Found:
		if(not(allProfessorDataFound)):
			#Specifically, Look In Next Section.
			sIndex += 1; 
			#If sIndex Within Bounds:
			if(sIndex < len(allSectionValues)):
				#Get Start of Instructor Data:
				startValue = self.__getProfessorStartValue(allSectionValues, sIndex);
				#"Instructor" Was In Previous Section, 
				#...Start Looking From First Piece of Information.
				if(startValue == None):
					startValue = 0;
				#Find Children + Pass To Populate Appropriate Data to allProfessorData
				currentChildren = allSectionValues[sIndex].findChildren();
				allProfessorDataFound = self.__putAllProfessorData(startValue, currentChildren);
				#Error Check If Not Found In Consecutive Section.
				if(not(allProfessorDataFound)):
					print("Fatal Error In Finding Missing Data In Conseuctive Section.")
					return (None, sIndex);
			else:
				#Could Not Ever Find Data.
				print("Fatal Error In Optimization For Missing Data.");
				return (None, sIndex);
		#Return Correctly Formatted/Reformatted Professor Data.
		return (self.__formatProfessorData(), sIndex);

	#Private Function:
	#Determines The Start Index of "Instructor" Data From A Particular Section.
	def __getProfessorStartValue(self, allSectionValues, sIndex):
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

	#Private Function:
	#Puts All Professor Data From Current Section Into self.allProfessorData. 
	#If Found All Information, Then Return True.
	#Else, Return False.
	def __putAllProfessorData(self, startValue, currentChildren):
		#Terminate w/ Keyword "Teaching Assistant(s)":
		for k in range(startValue, len(currentChildren)):
			#Replace '\xa0' with ' '
			currentInformation = currentChildren[k].get_text().replace('\xa0', ' ');
			if("Teaching Assistant(s) " == currentInformation):
				return True;
			else:
				#Populate Professor Data If Non-Empty:
				if(currentInformation != '' and currentInformation != ' '):
					self.allProfessorData.append(currentInformation);
		#Never Found "Teaching Assistant(s)" => Need To Look In Next Section For Missing Data.
		return False;
	
	#Private Function:
	#Formats All Professor Data After Computed In Its Entirity.
	#Invoked By computeAllProfessorData To Reset Professor Data
	#To Only Contain Needed/Necessary Data For Client.
	def __formatProfessorData(self):
		#Format Professor Data Prior To Entry Into SQLite3 Database.
		if(self.allProfessorData == None):
			return None;
		#Remove Trailing ' ' From All Instructor Data.
		for k in range(0, len(self.allProfessorData)):
			self.allProfessorData[k] = self.allProfessorData[k][:-1];
		#Name of Professor:
		pName = self.allProfessorData[1];
		#Convert Email To @rpi.edu Instead of @RPI.EDU By Converting To Lowecase:
		pEmail = self.allProfessorData[2].lower();
		#Obtain Professor Office Hour Location:
		pLocation = self.__getProfessorLocationValue(self.allProfessorData[3:]);
		#Obtain Professor Office Hour Data:
		pOfficeHours = self.__getProfessorOfficeHours(self.allProfessorData[3:]);	
		
		#Standardize/Normalize Professor Data:
		self.allProfessorData = [];
		self.allProfessorData.append(pName);
		self.allProfessorData.append(pEmail);
		self.allProfessorData.append(pLocation);
		self.allProfessorData.append(pOfficeHours);
		
		return self.allProfessorData;

	#Private Function:
	#Called By __formatProfessorData.
	#Determines The Office Location For The Professor.
	def __getProfessorLocationValue(self, currentDataToExamine):
		for k in range(0, len(currentDataToExamine)):
			if("Office Location: " in currentDataToExamine[k]):
				return currentDataToExamine[k][17:];
		return "Currently To Be Determined.";

	#Private Function:
	#Called By __formatProfessorData.
	#Determines All Office Hours For The Professor.
	#Returns List of Formatted Office Hours Data For Professor.  
	def __getProfessorOfficeHours(self, currentDataToExamine):
		#Find Start of Office Hours Data:
		startValue = None;
		currentOfficeHours = [];
		for k in range(0, len(currentDataToExamine)):
			if("Office Hours: " in currentDataToExamine[k]):
				startValue = k;
				currentDataToExamine[k] = currentDataToExamine[k][14:];
		#Case 1: No Office Data.
		if(startValue == None):
			return [("Not Applicable.","Currently To Be Determined.")];
		#Combine All Office Hours Data Into A Single STR.
		allDataInSingleStr = "";
		for k in range(startValue, len(currentDataToExamine)):
			allDataInSingleStr += currentDataToExamine[k];
			#Do Not Append Space To Very End of Data.
			if(k != len(currentDataToExamine)-1):
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
				(startTime, endTime) = getStartEndTimes(secondValue);
				if(startTime != None and endTime != None):
					currentOfficeHours.append((firstValue, startTime, endTime))
				k -= 1;
			#Case 2: Date Specified.
			else:
				#Case 3: Time Specified
				if(secondValue != None):
					(startTime, endTime) = getStartEndTimes(secondValue);
					if(startTime != None and endTime != None):
						currentOfficeHours.append((firstValue, startTime, endTime))
		#No Correct Office Hours Data Found:
		if(len(currentOfficeHours) == 0):
			return [("Not Applicable.","Currently To Be Determined.")];
		return currentOfficeHours;

#---------------------------------------------------------------------------------------------------

#This Class Is Used To Populate The Current Professor Data + Office Hours 
#From A Particular Section/Course Into Our Backend Django SQLite3 Database. 	
class PopulateForProfessor(object):
	
	#Constructor:
	#Contains Data To Be Populated:
	def __init__(self, currentProfessorData):
		self.allProfessorData = currentProfessorData;
	
	#Public Function:
	#Runs Population of self.allProfessorData Into Database.
	def runPopulateProfessorData(self, currentCourseAbbrev):
		#Checks/Asserts That Course Truly Exists When Called By scrapeSpring2019OfficeHours()
		allExistingCourses = Course.objects.filter(courseAbbrev = currentCourseAbbrev);
		#Since courseAbbrev = Unique Course Attribute, len(allExistingCourses) Must Be 1.
		currentCourseObject = allExistingCourses[0];
		allExistingProfessors = Professor.objects.filter(currentCourse = currentCourseObject).filter(pName = self.allProfessorData[0]);
		#Professor For PArticular Course Does Not Exist
		if(len(allExistingProfessors) == 0):
			currentProfessor = Professor(pName = self.allProfessorData[0], 
											pEmail = self.allProfessorData[1], 
											currentCourse = currentCourseObject);
			currentProfessor.save();
			#Loop Through All Professor Office Hours:
			for k in range(0, len(self.allProfessorData[3])):
				#Check That Specific Office Hours Do Not Yet Exist:
				allExistingOfficeHours = ProfessorOfficeHours.objects.filter(meetProfessor = currentProfessor)
				allExistingOfficeHours = allExistingOfficeHours.filter(meetLocation = self.allProfessorData[2])
				allExistingOfficeHours = allExistingOfficeHours.filter(meetDates = self.allProfessorData[3][k][0])
				allExistingOfficeHours = allExistingOfficeHours.filter(meetStartTime = self.allProfessorData[3][k][1])
				allExistingOfficeHours = allExistingOfficeHours.filter(meetEndTime = self.allProfessorData[3][k][2]);
				if(len(allExistingOfficeHours) == 0):
					newOfficeHours = ProfessorOfficeHours(meetProfessor = currentProfessor,
															meetLocation = self.allProfessorData[2],
															meetDates = self.allProfessorData[3][k][0],
															meetStartTime = self.allProfessorData[3][k][1],
															meetEndTime = self.allProfessorData[3][k][2]);
					newOfficeHours.save();
		else:
			currentProfessor = allExistingProfessors[0];
			#Loop Through All Professor Office Hours:
			for k in range(0, len(self.allProfessorData[3])):
				#Check That Specific Office Hours Do Not Yet Exist:
				allExistingOfficeHours = ProfessorOfficeHours.objects.filter(meetProfessor = currentProfessor)
				allExistingOfficeHours = allExistingOfficeHours.filter(meetLocation = self.allProfessorData[2])
				allExistingOfficeHours = allExistingOfficeHours.filter(meetDates = self.allProfessorData[3][k][0])
				allExistingOfficeHours = allExistingOfficeHours.filter(meetStartTime = self.allProfessorData[3][k][1])
				allExistingOfficeHours = allExistingOfficeHours.filter(meetEndTime = self.allProfessorData[3][k][2]);
				if(len(allExistingOfficeHours) == 0):
					newOfficeHours = ProfessorOfficeHours(meetProfessor = currentProfessor,
															meetLocation = self.allProfessorData[2],
															meetDates = self.allProfessorData[3][k][0],
															meetStartTime = self.allProfessorData[3][k][1],
															meetEndTime = self.allProfessorData[3][k][2]);
					newOfficeHours.save();

#---------------------------------------------------------------------------------------------------

#Main Driver Scrape Class For All Formats:
class Scrape(object):

	#Scrape All Spring 2020 Courses + Course Sections + Meeting Time Data:
	def scrapeSpring2020Courses(self):
		#Clear Database Prior To Population:
		currentDataInDatabase = Course.objects.all()
		if(len(currentDataInDatabase) != 0):
			currentDataInDatabase.delete()
		currentParserForCourses = ParseForCourse();
		currentParserForCourses.computeAllCourseData();
		allCourseData = currentParserForCourses.allCourseData;
		currentPopForCourse = PopulateForCourse(allCourseData);
		currentPopForCourse.runPopulateCourseData();

	#Scrape All Spring 2019 Professor + TA Office Hours:
	def scrapeSpring2019OfficeHours(self):
		#Clear/Flush Database Objects Prior To Population.
		currentProfessorDataInDatabase = Professor.objects.all()
		if(len(currentProfessorDataInDatabase) != 0):
			currentProfessorDataInDatabase.delete()
		#Begin Scrape Procedure:
		with open("prevSyllabus.html", "r") as currentFileReader:
			#Read + Obtain All PDF Data:
			currentPDFData = currentFileReader.read()
			currentSoup = BeautifulSoup(currentPDFData, 'html.parser')
			#Find All Subsections For Course Information:
			allSectionValues = currentSoup.find_all("div")
			#Loop Through All Course Descriptions:
			k = 0;
			countFoundData = 0;
			while(k < len(allSectionValues)):
				currentSection = allSectionValues[k];
				#Check If Current Section Contains Instructor Information:
				if(currentSection.find_all("p", string=re.compile("Instructor")) != None):
					currentParserForCourse = ParseForCourseAbbrev();
					currentParserForCourse.computeCourseAbbrevName(allSectionValues, k);
					currentCourseAbbrev = currentParserForCourse.currentIdentityValue;
					#Assert Current Section Describes A Valid Section:
					if(currentCourseAbbrev != None):
						print(currentCourseAbbrev)
						currentParserForProfessor = ParseForProfessor();
						allProfessorData, sIndex = currentParserForProfessor.computeAllProfessorData(allSectionValues, k);
						print(allProfessorData)
						currentPopForProfessor = PopulateForProfessor(allProfessorData);
						currentPopForProfessor.runPopulateProfessorData(currentCourseAbbrev);
						k = sIndex;
						countFoundData += 1;
						print()
				k += 1;
			print(countFoundData);

#---------------------------------------------------------------------------------------------------

#Main Function:
#Invokes Appropriate Scrape Objects.
def main():
	#Error Checking For # of Arguments:
    if(len(sys.argv) < 2):
    	print("Incorrect Number of Arguments.")
    	return
    else:
    	scrapeValue = int(sys.argv[1])
    	currentScrape = Scrape()
    	#"0" = Scrape Spring 2020 Course Data
    	if(scrapeValue == 0):
    		print("Start of Scrape Spring 2020 Course Data.")
    		currentScrape.scrapeSpring2020Courses()
    		print("Termination of Scrape Spring 2020 Course Data.")
    	#"!=0" = Scrape Spring 2019 Syllabus Data
    	else:
    		print("Start of Scrape Spring 2019 Office Hours Data.")
    		currentScrape.scrapeSpring2019OfficeHours()
    		print("Termination of Scrape Spring 2019 Office Hours Data.")

if __name__ == "__main__":
    main()