import shared

from manageData import ManageData
from travellingPlane import TravellingPlane

manageData = ManageData()

manageData.loadData("matlab/test.csv")
manageData.plotData("origionalData")
manageData.sortData(TravellingPlane)
manageData.plotData("sortedData")

manageData.loadData()
manageData.plotData("origionalMatlabData")
manageData.sortData(TravellingPlane)
manageData.plotData("sortedMatlabData")

manageData.updateData()
manageData.loadData()
manageData.plotData("origionalMatlabData")
manageData.sortData(TravellingPlane)
manageData.plotData("sortedMatlabData")