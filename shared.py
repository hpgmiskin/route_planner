import re,csv,numpy,math,operator,itertools,math,operator

DEBUG = False
gravity = 9.81
mass = 10

def naturalKeys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''

    def atoi(text):
        return int(text) if text.isdigit() else text

    return [ atoi(c) for c in re.split('(\d+)', text) ]

def changeArray(array):
    """function that cahgnes the configuration of an array 

    given input: [[a1,b1,c1],[a2,b2,c2]]
    returns: [[a1,a2],[b1,b2],[c1.c2]]

    """

    return [[float(array[j][i]) for j in range(len(array))] for i in range(len(array[0]))]

def loadData(filename):
    "loads the data in the given file into a dictionary where the coloumb headings are the keys"

    with open(filename,"r") as csvFile:
        csvReader = csv.reader(csvFile,dialect="excel")

        data = {}
        for i,row in enumerate(csvReader):
            if (i == 0):
                columbNames = []
                for item in row:
                    columbNames.append(item)
                    data[item] = []
            else:
                for j,item in enumerate(row):
                    data[columbNames[j]].append(float(item))

    return data

def saveData(filename,data):
    """function to save the given data as a CSV file

    only writes the shortest data set in dictionary

    dictionary key is columb name and value is array
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

if __name__ == "__main__":
    nodes = latinHypercube(12)
    print(nodes)
    [x,y,z] = changeArray(nodes)
    print(x,y,z)