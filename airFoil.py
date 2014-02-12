# code to get the data for certain airfoils

import re,urllib.request

class AirFoil():
	"""class to load airfoil data and return the lift and drag values depending on the angle of attack"""

	def __init__(self, foilName="naca23015-il", reynoldsNumber=50000):
		"initiates the class by calling setFoilData that populates alpha, CL and CD"

		self.AoAs = []
		self.CDs = []
		self.CLs = []
		
		self.setFoilData(foilName,reynoldsNumber)

	def getCL(self,alpha):
		"returns the closes approximation of the coeficient of lift given the angle of attack alpha"

		difference = [abs(AoA-alpha) for AoA in self.AoAs]
		minimumIndex = difference.index(min(difference))

		return self.CLs[minimumIndex]

	def getCD(self,alpha):
		"returns the closes approximation of the coeficient of drag given the angle of attack alpha"

		difference = [abs(AoA-alpha) for AoA in self.AoAs]
		minimumIndex = difference.index(min(difference))

		return self.CDs[minimumIndex]

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
		with urllib.request.urlopen(url) as webPage:
			content = webPage.read().splitlines()

		#set not to record data until certain point
		record = False

		#cycle through lines of content to obtain alpha, CD and CL
		for row in content:
			row = str(row)
			rowList = re.split(r'\s*',row)

			if (record and ("--" not in row)):
				self.AoAs.append(float(rowList[1]))
				self.CLs.append(float(rowList[2]))
				self.CDs.append(float(rowList[3]))

			if (("alpha" == rowList[1]) and ("CL" == rowList[2]) and ("CD" == rowList[3])):
				record = True

if __name__ == "__main__":
	airFoil = AirFoil("naca23015-il",100000)
	print(airFoil.getCD(8.25))