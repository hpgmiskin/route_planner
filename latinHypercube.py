#latinHypercube
import numpy,os,sys,csv,subprocess

MATLAB_FILEPATH = "update_data.m"
MATLAB_OUTPUT_FILEPATH = "matlab_output"

def unitCube(numberPoints):
    "function to return the nodes contained within a latin hypercube of given size"

    return samplePlan(3,numberPoints)

    filePath = "matlab/{}_{}.csv".format(MATLAB_OUTPUT_FILEPATH,numberPoints)

    def updateMatlab(numberPoints):
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

    def loadMatlab(filePath):
        "function to load the data created by MATLAB"

        nodes = []
        with open(filePath,"r") as csvFile:
            csvReader = csv.reader(csvFile,dialect="excel")
            for row in csvReader:
                node = [float(item) for item in row[:3] if len(item)>0]
                if (len(node) == 3):
                    nodes.append(node)

        return [numpy.array(node) for node in nodes]

    try:
        open(filePath)
    except FileNotFoundError:
        updateMatlab(numberPoints)

    return loadMatlab(filePath)

def samplePlan(numberDimensions,numberPoints):
    "function to return the nodes contained within a latin hypercube of given size"

    filePath = "matlab/latin_hypercube_{}_{}.csv".format(numberDimensions,numberPoints)

    def updateMatlab():
        """function to run the required matlab script that updates all required data

        assumes that the function to update matlab is stored in a folder called matlab of current directory
        """

        fileContents = ""
        fileContents+="output = bestlh({},{},1,1);\n".format(numberPoints,numberDimensions)
        fileContents+="csvwrite('latin_hypercube_{}_{}.csv',output);".format(numberDimensions,numberPoints)

        with open("matlab/"+MATLAB_FILEPATH,"w") as openFile:
            openFile.write(fileContents)

        filePath = "matlab/"+MATLAB_FILEPATH
        currentDirectory = os.getcwd()
        matlabCommand = 'cd {}, run {}, exit'.format(currentDirectory,filePath)

        subprocess.check_call(['matlab', '-wait', '-automation', '-nosplash', '-noFigureWindows', '-r', matlabCommand])

    def loadMatlab():
        "function to load the data created by MATLAB"

        nodes = []
        with open(filePath,"r") as csvFile:
            csvReader = csv.reader(csvFile,dialect="excel")
            for row in csvReader:
                node = [float(item) for item in row[:3] if len(item)>0]
                if (len(node) == 3):
                    nodes.append(node)

        return [numpy.array(node) for node in nodes]

    try:
        open(filePath)
    except FileNotFoundError:
        updateMatlab(numberPoints)

    return loadMatlab(filePath)

def sampleSpace(xLength,yLength,zLength,numberPoints):
	"function to return a latin hypercube scaled to the required sample size and with the given number of points"

	nodes = unitCube(numberPoints)

	scaledNodes = numpy.zeros([numberPoints,3])
	for i,node in enumerate(nodes):
		[x,y,z] = node
		scaledNodes[i] = [x*xLength,y*yLength,z*zLength]

	return scaledNodes


