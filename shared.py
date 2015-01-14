import os,re,csv,numpy,math,operator,itertools,math,operator,json,collections

#global debug variable
DEBUG = False

#global variables used in computations
MAX_LENGTH = 1000
LOWEST_NODE = 20
HIGHEST_NODE = 220
ALL_NODES = list(range(LOWEST_NODE,HIGHEST_NODE+1))
ALL_BETAS = [round(0.1*item,1) for item in range(1,5)]

def naturalKeys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
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

def loadOrRun(filename,function,*args):
    """load run attempts to open the given filename and if this is possible returns the data
    if the filename is not accessible for some reason loadRun runs the given function with inputs args
    the returned result is saved as a JSON
    """
    def loadJSON(filename):
        "saves the data object as a JSON string"
        with open(filename,"r") as openFile:
            data = json.loads(openFile.read())
        return data

    def saveJSON(filename,data):
        "saves the data object as a JSON string"
        with open(filename,"w") as openFile:
            openFile.write(json.dumps(data))
    try:
        data = loadJSON(filename)
    except IOError:
        data = function(*args)
        saveJSON(filename,data)

    return data

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
                    if (len(item) > 0):
                        data[columbNames[j]].append(float(item))

    for key,value in data.items():
        if ((type(value) == list) and (len(value)==1)):
            data[key] = value[0]

    return data

def saveData(filename,data):
    """function to save the given data as a CSV file
    only writes the shortest data set in dictionary
    dictionary key is columb name and value is array
    """

    if (type(data) != dict):
        raise ValueError("The function provided did not return a single dictionary")
    elif not all([isinstance(data[key], collections.Iterable) for key in data.keys()]):
        try:
            for key,value in data.items():
                if (type(value) != list):
                    data[key] = [value]
        except Exception as exception:
            raise ValueError("The function returned a dictionary with values that arent lists {}".format(exception))

    with open(filename, 'w') as csvfile:
        csvWriter = csv.writer(csvfile, dialect="excel")

        columbNames = []

        for key in data.keys():
            columbNames.append(key)

        csvWriter.writerow(columbNames)

        numberRows = max([len(data[key]) for key in columbNames])
        coloumbValues = [coloumbValue+[None]*(numberRows-len(coloumbValue)) for coloumbValue in data.values()]

        for i in range(numberRows):
            row = [item[i] for item in coloumbValues]
            csvWriter.writerow(row)

def calculateEnergy(distance,height,beta):
    """calculates and returns the energy required to travel between two points

    beta represents the distance climb ratio 
    beta = 1: distance is equal weighting to height gain
    beta = 0: only height gain is considered
    """

    #check if height change is too great
    if (abs(height) > distance):
        return numpy.infty

    energy = beta*distance + height

    return max([0,energy])
