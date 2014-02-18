# code to get the data for certain airfoils

import numpy,re,urllib.request
from shared import *

class AirFoil():
	"""class to load airfoil data and return the lift and drag values depending on the angle of attack"""

	def __init__(self, foilName="naca23015-il", reynoldsNumber=50000):
		"initiates the class by calling setFoilData that populates alpha, CL and CD"

		self.foilName = foilName
		self.reynoldsNumber = reynoldsNumber
		self.AoAs = []
		self.CDs = []
		self.CLs = []
		self.CLCDs = []
		
		self.setFoilData(foilName,reynoldsNumber)

	def plotData(self):
		"method to plot the range of efficiency values for the airfoil"

		xAxis = numpy.linspace(min(self.AoAs),max(self.AoAs),100)
		yAxis = []

		for alpha in xAxis:
			yAxis.append(self.getEfficiency(alpha))

		filename = self.reynoldsNumber#"Reynolds Number - {}".format(self.reynoldsNumber)

		return filename,xAxis,yAxis
		
	def getIndex(self,alpha):
		"returns the index of the value where alpha is closest to the angle of attack"

		difference = [abs(AoA-alpha) for AoA in self.AoAs]
		minimumDifference = min(difference)

		#check if angle of attack is not close enough to the lookup value
		if (minimumDifference > 1):
			print("stall")
			#raise ValueError("This angle of attack would induce stall")

		index = difference.index(minimumDifference)

		return index

	def getCL(self,alpha):
		"returns the closes approximation of the coeficient of lift given the angle of attack alpha"

		return self.CLs[self.getIndex(alpha)]

	def getCD(self,alpha):
		"returns the closes approximation of the coeficient of drag given the angle of attack alpha"

		return self.CDs[self.getIndex(alpha)]

	def getEfficiency(self,alpha):
		"returns the closest approximation of the efficiency given the angle of attack alpha"

		return self.CLCDs[self.getIndex(alpha)]

	def setEfficiency(self):
		"sets the efficiency of the airfoil for diffrent angles of attack where efficiency = CL/CD"

		self.CLCDs = [self.CLs[i]/self.CDs[i] for i in range(min([len(self.CLs),len(self.CDs)]))]

	def setFoilData(self,foilName,reynoldsNumber):
		"returns a dictionary of the airfoils lift and drag coeficients at differnt angles of attack"

		#load list of foil names
		with open("airfoils.txt") as openFile:
			airfoils = openFile.read().splitlines()

		#check requested foil is in list
		if (foilName not in airfoils):
			raise ValueError("Foil name {} does not exist".format(foilName))

		#check requested reynoldy number exists
		reynoldsNumbers = [50000,100000,200000,500000,1000000]
		if (reynoldsNumber not in reynoldsNumbers):
			raise ValueError("Reynoldy number {} does not exist".format(reynoldsNumber))

		#access the data file
		url = 'http://airfoiltools.com/polar/text?polar=xf-{}-{}'.format(foilName,reynoldsNumber)
		#print(url)
		with urllib.request.urlopen(url) as webPage:
			content = webPage.read().splitlines()

		#set not to record data until certain point
		record = False

		#cycle through lines of content to obtain alpha, CD and CL
		for row in content:
			row = str(row)
			rowList = re.split(r'\s*',row)
			#print(row)

			if (record and ("--" not in row)):
				self.AoAs.append(float(rowList[1]))
				self.CLs.append(float(rowList[2]))
				self.CDs.append(float(rowList[3]))

			if (("alpha" == rowList[1]) and ("CL" == rowList[2]) and ("CD" == rowList[3])):
				record = True

		self.setEfficiency()

if __name__ == "__main__":

	#naca23015-il
	#sd7037-il

	airfoil = "naca23015-il"
	xAxis = {}
	yAxis = {}

	for reynoldsNumber in [50000,100000,200000,500000,1000000]:

		filename,x,y = AirFoil(airfoil,reynoldsNumber).plotData()

		xAxis[filename] = x
		yAxis[filename] = y

	xLabel = "Angle of Attack"
	yLabel = "Efficiency"

	plot2dFigure(airfoil,xAxis,yAxis,xLabel,yLabel,True)