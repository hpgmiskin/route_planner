import math,operator

DEBUG = False
G = 9.81

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