import os,sys,csv,subprocess,math,operator
from shared import *

MATLAB_FILEPATH = "update_data.m"
MATLAB_OUTPUT_FILEPATH = "matlab_output"

class ManageData():
	"""docstring for Data"""

	def __init__(self,update=False):

		if update:
			self.updateData()

	def updateData(self,numberPoints=10):
		"""function to run the required matlab script that updates all required data

		assumes that the function to update matlab is stored in a folder called matlab of current directory
		"""

		fileContents = ""
		fileContents+="output = bestlh({},3,1,1);\n".format(numberPoints)
		fileContents+="csvwrite('{}_{}.csv',output);".format(MATLAB_OUTPUT_FILEPATH,numberPoints)

		with open("matlab/"+MATLAB_FILEPATH,"w") as openFile:
			openFile.write(fileContents)

		filePath = "matlab/"+MATLAB_FILEPATH
		currentDirectory = os.getcwd()
		matlabCommand = 'cd {}, run {}, exit'.format(currentDirectory,filePath)

		subprocess.check_call(['matlab', '-wait', '-automation', '-nosplash', '-noFigureWindows', '-r', matlabCommand])

	def loadData(self,numberPoints=10):
		"function to load the data created by MATLAB"

		filePath = "matlab/{}_{}.csv".format(MATLAB_OUTPUT_FILEPATH,numberPoints)

		nodes = []
		with open(filePath,"r") as csvFile:
			csvReader = csv.reader(csvFile,dialect="excel")
			for row in csvReader:
				node = [float(item) for item in row[:3] if len(item)>0]
				if (len(node) == 3):
					nodes.append(node)

		self.nodes = nodes

	def sortData(self,sortFunction):
		"""method to sort cylindrical coordinates using travelling salesman"""

		nodes = self.nodes

		sortFunction.setNodes(nodes,3)
		order = sortFunction.getOrder()

		sortedNodes = []
		for index in order:
			sortedNodes.append(nodes[index])

		#sortedNodes.append(nodes[order[0]])

		self.nodes = sortedNodes

	def plotData(self,filename=""):
		"method to plot the data"

		nodes = self.nodes
		plotData = changeArray(nodes)
		plotFigure(filename,plotData,True)

if __name__ == "__main__":
	manageData = ManageData()
	manageData.loadData("matlab/test.csv")
