# code to get the data for certain airfoils

import re,urllib.request

def getFoilData(foilName=None,reynoldsNumber=None):
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
	#construct dictionary to hold cvalues
	result = {"alpha":[],"CL":[],"CD":[]}

	#cycle through lines of content to obtain alpha, CD and CL
	for row in content:
		row = str(row)
		rowList = re.split(r'\s*',row)

		if (record and ("--" not in row)):
			result["alpha"].append(float(rowList[1]))
			result["CL"].append(float(rowList[2]))
			result["CD"].append(float(rowList[3]))

		if (("alpha" == rowList[1]) and ("CL" == rowList[2]) and ("CD" == rowList[3])):
			record = True

	return result

if __name__ == "__main__":
	result = getFoilData("ag45c03-il",50000)

	print(result["alpha"])
	print(result["CD"])
	print(result["CL"])