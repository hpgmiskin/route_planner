from shared import *
import numpy,re,urllib2

class AirFoil():
	"""class to load airfoil data and return the lift and drag values depending on the angle of attack"""

	def __init__(self, foilName, reynoldsNumber=1000000):
		"initiates the class by calling setFoilData that populates alpha, CL and CD"
	
		self.setFoilData(foilName,reynoldsNumber)

	def getAoAs(self):
		"returns all possible angles of attacks possible"

		return numpy.array(self.AoAs)

	def getCLs(self):
		"returns all values for the coeficient of lift"

		return numpy.array(self.CLs)

	def getCDs(self):
		"returns all values for the zero lift coeficient of drag"

		return numpy.array(self.CDs)

	def setReynoldsNumber(self,reynoldsNumber=1000000):
		"method to set reynolds number after constructing class"

		self.setFoilData(self.foilName,reynoldsNumber)
		return self.reynoldsNumber

	def setFoilData(self,foilName,reynoldsNumber):
		"returns a dictionary of the airfoils lift and drag coeficients at differnt angles of attack"

		self.foilName = foilName
		self.reynoldsNumber = reynoldsNumber
		self.AoAs = []
		self.CDs = []
		self.CLs = []

		#load list of foil names
		with open("airfoils.txt") as openFile:
			airfoils = openFile.read().splitlines()

		#check requested foil is in list
		if (foilName not in airfoils):
			raise ValueError("Foil name {} does not exist".format(foilName))

		#if reynolds number not in list use closest estimate
		reynoldsNumbers = [50000,100000,200000,500000,1000000]
		if (reynoldsNumber not in reynoldsNumbers):
			difReynoldsNumbers = [abs(reynoldsNumber-item) for item in reynoldsNumbers]
			self.reynoldsNumber = reynoldsNumbers[difReynoldsNumbers.index(min(difReynoldsNumbers))]

		#access the data file
		url = 'http://airfoiltools.com/polar/text?polar=xf-{}-{}'.format(self.foilName,self.reynoldsNumber)
		page = urllib2.urlopen(url)
                content = page.read().splitlines()

		#set not to record data until certain point
		record = False

		#cycle through lines of content to obtain alpha, CD and CL
		for row in content:

			#split row by space characters
			row = str(row)
			rowList = re.split(r'\s*',row)

			#if recording is true and not line break line save values
			if (record and ("--" not in row)):
				self.AoAs.append(float(rowList[1]))
				self.CLs.append(float(rowList[2]))
				self.CDs.append(float(rowList[3]))

			#if columb headers found set recording to True
			if (("alpha" == rowList[1]) and ("CL" == rowList[2]) and ("CD" == rowList[3])):
				record = True

		self.AoAs = numpy.array(self.AoAs)
		self.CDs = numpy.array(self.CDs)
		self.CLs = numpy.array(self.CLs)
