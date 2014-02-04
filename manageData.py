import os,sys,csv,subprocess,math,operator
from shared import *

def getGraphLogicPath():
	"function to return the graph_logic path"

	cwd = os.getcwd()
	rootPath = os.path.dirname(cwd)
	newPath = os.path.join(rootPath,"graph_logic")

	return newPath

sys.path.insert(0, getGraphLogicPath())

MATLAB_FILEPATH = "matlab/update_data"
MATLAB_OUTPUT_FILEPATH = "matlab/matlab_output.csv"

class manageData():
	"""docstring for Data"""

	def __init__(self,filePath,inputData=None):

		self.filePath = filePath

		if inputData:
			self.setData(inputData)
		else:
			self.loadData()

		self.setCentre()
		self.sortData()

	def updateData(self):
		"""function to run the required matlab script that updates all required data

		assumes that the function to update matlab is stored in a folder called matlab of current directory
		"""

		filePath = MATLAB_FILEPATH
		currentDirectory = os.getcwd()
		matlabCommand = 'cd {}, run {}, exit'.format(currentDirectory,filePath)

		subprocess.check_call(['matlab', '-wait', '-automation', '-nosplash', '-noFigureWindows', '-r', matlabCommand])

	def loadData(self):
		"function to load the data created by MATLAB"

		data = []
		filePath = self.filePath
		with open(filePath,"r") as csvFile:
			csvReader = csv.reader(csvFile,dialect="excel")
			for row in csvReader:
				data.append([float(item) for item in row])

		self.xyz = changeArray(data)

	def sortData(self):
		"""method to sort cylindrical coordinates using travelling salesman"""

		rtz = self.rtz
		r,t,z = rtz[0],rtz[1],rtz[2]
		length = range(min(len(r),len(t),len(z)))

		nodes = [(r[i],t[i],z[i]) for i in length]
		#print(nodes)
		#order = travellingSalesman(nodes,"rtz")
		order = travellingPlane(nodes)
		#print(order)

		#print(order)

		newR,newT,newZ = [],[],[]

		for i in range(len(order)):
			index = int(order[i]) - 1
			#print(index)

			newR.append(r[index])
			newT.append(t[index])
			newZ.append(z[index])

		self.rtz = [newR,newT,newZ]