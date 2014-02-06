import shared

from manageData import ManageData
from travellingPlane import TravellingPlane

manageData = ManageData()
manageData.loadData("matlab/test.csv")
manageData.plotData("origionalData.png")
manageData.sortData(TravellingPlane)
manageData.plotData("sortedData.png")