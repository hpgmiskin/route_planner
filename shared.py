import numpy,math,operator,itertools,os,sys,csv,subprocess,math,operator

DEBUG = False
gravity = 9.81
mass = 10

MATLAB_FILEPATH = "update_data.m"
MATLAB_OUTPUT_FILEPATH = "matlab_output"

def changeArray(array):
    """function that cahgnes the configuration of an array 

    given input: [[a1,b1,c1],[a2,b2,c2]]
    returns: [[a1,a2],[b1,b2],[c1.c2]]

    """

    return [[float(array[j][i]) for j in range(len(array))] for i in range(len(array[0]))]

def loadData(filename):
    "loads the data in the given file into a dictionary where the coloumb headings are the keys"

    with open(filePath,"r") as csvFile:
        csvReader = csv.reader(csvFile,dialect="excel")

        columbNames = csvReader[0]
        data = {}

        for item in columbNames:
            data[item] = []

        for row in csvReader[1:]:
            for i,item in enumerate(row):
                data[columbNames[i]].append(round(item))


    return data

def saveData(filename,data):
    """function to save the given data as a CSV file

    only writes the shortest data
    """

    with open(filename, 'w', newline='') as csvfile:
        csvWriter = csv.writer(csvfile, dialect="excel")

        columbNames = []

        for key in data.keys():
            columbNames.append(key)

        csvWriter.writerow(columbNames)

        numberRows = min([len(data[key]) for key in columbNames])

        for i in range(numberRows):
            row = [item[i] for item in data.values()]
            csvWriter.writerow(row)


def calculateEnergy(distance,height):
    "calculates and returns the energy required to travel between two points"

    #check if height change is too great
    if (abs(height) > distance):
        return numpy.infty

    #define function for drag force
    def dragForce(velocity):
        "returns the drag force of a standard UAV given the velocity"
        return velocity*11/14

    dragEnergy = distance*dragForce(10)
    gravityEnergy = mass*gravity*height
    totalEnergy = dragEnergy + gravityEnergy

    return max([0,totalEnergy])

def latinHypercube(numberPoints):
    "function to return the nodes contained within a latin hypercube of given size"

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

        return nodes

    try:
        open(filePath)
    except FileNotFoundError:
        updateMatlab(numberPoints)

    return loadMatlab(filePath)

if __name__ == "__main__":
    nodes = latinHypercube(12)
    print(nodes)
    [x,y,z] = changeArray(nodes)
    print(x,y,z)