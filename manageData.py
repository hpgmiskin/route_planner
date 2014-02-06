import os,sys,csv,subprocess,math,operator
from shared import *

MATLAB_FILEPATH = "matlab/update_data"
MATLAB_OUTPUT_FILEPATH = "matlab/matlab_output.csv"

class ManageData():
	"""docstring for Data"""

	def __init__(self,update=False):

		if update:
			self.updateData()
			self.loadData(MATLAB_OUTPUT_FILEPATH)

	def updateData(self):
		"""function to run the required matlab script that updates all required data

		assumes that the function to update matlab is stored in a folder called matlab of current directory
		"""

		filePath = MATLAB_FILEPATH
		currentDirectory = os.getcwd()
		matlabCommand = 'cd {}, run {}, exit'.format(currentDirectory,filePath)

		subprocess.check_call(['matlab', '-wait', '-automation', '-nosplash', '-noFigureWindows', '-r', matlabCommand])

	def loadData(self,filePath):
		"function to load the data created by MATLAB"

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
		order = sortFunction(nodes).getOrder()

		sortedNodes = []
		for index in order:
			sortedNodes.append(nodes[index])

		sortedNodes.append(nodes[order[0]])

		self.nodes = sortedNodes

	def plotData(self,filename):
		"method to plot the data"

		nodes = self.nodes
		plotData = changeArray(nodes)
		plotFigure(filename,plotData)

if __name__ == "__main__":
	manageData = ManageData()
	manageData.loadData("matlab/test.csv")