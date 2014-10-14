from shared import *
import numpy,os,sys,csv,subprocess,time

def unitCube(numberOfNode):
	"function to return the nodes contained within a unit latin hypercube with given numbers of nodes"

	return samplePlan(3,numberOfNode)

def allUnitCubes():
	"function to calculate all unit cube latin hypercubes"

	for i in ALL_RESULTS:
		unitCube(i)

def samplePlan(numberDimension,numberOfNode):
	"function to load or compute latin hypercubes of given number of nodes and dimensions"

	numberDimension = int(numberDimension)
	numberOfNode = int(numberOfNode)
	matlabUpdate = "update_data.m"

	#if less than two nodes return None
	if (numberOfNode < 2):
		return None

	def updateMatlab(numberDimension,numberOfNode):
		"""function to run the required matlab script that updates all required data

		assumes that the function to update matlab is stored in a folder called matlab of current directory
		"""

		#define matlab update file
		fileContents = ""
		fileContents+="output = bestlh({},{},1,1);\n".format(numberOfNode,numberDimension)
		fileContents+="csvwrite('latin_hypercube_{}_{}.csv',output);".format(numberDimension,numberOfNode)

		#write update file for matlab to call
		updatePath = "matlab/update_data.m"
		with open(updatePath,"w") as openFile:
			openFile.write(fileContents)

		#define command to call matlab in current working directory and run update file
		currentDirectory = os.getcwd()
		matlabCommand = 'cd {}, run {}, exit'.format(currentDirectory,updatePath)

		#run command with no windows or spash screen
		subprocess.check_call(['matlab', '-wait', '-automation', '-nosplash', '-noFigureWindows', '-r', matlabCommand])

	def loadMatlab(filePath):
		"function to load the data created by MATLAB"

		#for all rows in the output file
		nodes = []
		with open(filePath,"r") as csvFile:
			csvReader = csv.reader(csvFile,dialect="excel")
			for row in csvReader:
				nodes.append([float(item) for item in row if len(item)>0])

		#return numpy array of node coordinates
		return [numpy.array(node) for node in nodes]

	filePath = "matlab/latin_hypercube_{}_{}.csv".format(numberDimension,numberOfNode)
	try:
		#attempt to open the required hypercube
		open(filePath)
	except FileNotFoundError:
		#if file not found update matlab and wait for a second
		updateMatlab(numberDimension,numberOfNode)
		time.sleep(1)

	return loadMatlab(filePath)

def sampleSpace(lengths,numberOfNode):
	"function to return a latin hypercube scaled to the required sample size and with the given number of points"

	#define number of dimensions from length of lengths
	dimensions = len(lengths)
	#obtain the required number of nodes of given dimensions
	nodes = samplePlan(dimensions,numberOfNode)
	#create numpy array of lengths for easy dot product multiplication
	lengths = numpy.array(lengths)
	#preallocate memory for scaled nodes
	scaledNodes = numpy.zeros([numberOfNode,dimensions])

	#for all nodes populate scaled nodes
	for i,node in enumerate(nodes):
		scaledNodes[i] = node*lengths

	return scaledNodes

if (__name__ == "__main__"):
	allUnitCubes()
