import numpy,math,operator,itertools

import matplotlib
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as pyplot

DEBUG = False
gravity = 9.81
mass = 10

def factorial(n):
    "function to return the factorial of a number"
    
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def average(inputList):
    "returns the average of the list"

    if ((type(inputList) != list) or (len(inputList) < 1)):
        return inputList

    return sum(inputList)/len(inputList)

def addLists(listA,listB):
    "adds the list indices together and returns a list"

    if (len(listA) != len(listB)):
        raise ValueError("lists need to be of the same length")

    newList = [listA[i]+listB[i] for i in range(len(listA))]
    
    return newList

def negativeList(inputList):
    "returns the negative version of the list"

    return [-i for i in inputList]

def changeArray(array):
    """function that cahgnes the configuration of an array 

    given input: [[a1,b1,c1],[a2,b2,c2]]
    returns: [[a1,a2],[b1,b2],[c1.c2]]

    """

    return [[float(array[j][i]) for j in range(len(array))] for i in range(len(array[0]))]

def sortListOfTuples(listOfTuples,index=2,change=False):
    "sorts and returns the given list of tuples by the given index"

    if change:
        listOfTuples = changeArray(listOfTuples)

    listOfTuples.sort(key = operator.itemgetter(index))

    if change:
        listOfTuples = changeArray(listOfTuples)

    return listOfTuples

def calculateEnergy(deltaX,deltaY,deltaZ):
    "calculates and returns the energy required to travel between two points"

    def dragForce(velocity):
        "returns the drag force of a standard UAV given the velocity"
        return velocity*11/14

    distance = sum([deltaX**2,deltaY**2,deltaZ**2])**0.5
    dragEnergy = distance*dragForce(10)
    gravityEnergy = mass*gravity*deltaZ
    totalEnergy = dragEnergy + gravityEnergy

    return max([0,totalEnergy])

def permutation(nodes,nodeA=None,nodeB=None):
    """function to display the possible permutation sets for 2 routes
    starting at node index nodeA and node index nodeB in set nodes"""

    N = len(nodes)

    if (N%2 != 0):
        raise ValueError("N needs to be an even number of nodes") 
    routeLength = N//2

    permutationA=[]
    permutationB=[]

    for item in itertools.permutations(nodes,routeLength):

        if ((nodeA == item[0]) or (nodeA == None)):
            permutationA.append(item)
        elif ((nodeB == item[0]) or (nodeB == None)):
            permutationB.append(item)

    #print(permutationA)
    #print(permutationB)

    def checkRoutes(routeA,routeB):
        """checks the given routes to see if any nodes are repeated

        returns True if exclusive
        returns False if any repetition
        """

        for node in routeA:
            if (node in routeB):
                return False

        return True

    permutations = []

    for routeA in permutationA:
        for routeB in permutationB:

            if checkRoutes(routeA,routeB):
                permutations.append([routeA,routeB])

    return permutations


def plot2dFigure(filename,xAxis,yAxis,xLabel="",yLabel="",show=True):
    "method to plot the class data and if DEBUG = False save the figure"

    pyplot.figure(num=filename)
    pyplot.hold(True)
    pyplot.title(filename)

    for name,data in yAxis.items():
        pyplot.plot(xAxis[:len(data)],data,label=name)

    pyplot.xlabel(xLabel)
    pyplot.ylabel(yLabel)
    pyplot.legend()

    pyplot.show()

def plot3dFigure(filename,plotData,show=True):
    "method to plot the class data and if DEBUG = False save the figure"

    matplotlib.rcParams['legend.fontsize'] = 10

    fig = pyplot.figure(num=filename)
    ax = fig.gca(projection='3d')

    x,y,z = plotData[0],plotData[1],plotData[2]
    
    ax.plot(x, y, z, label=filename)
    ax.legend()

    if show:
        fig.show()
    else:
        fig.savefig(filename+".png")
    