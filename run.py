import shared

from manageData import ManageData
from travellingPlane import TravellingPlane

manageData = ManageData()
numberPoints = 4
#manageData.updateData(numberPoints)
name = "test_"+str(numberPoints)

sort = "greedy"
manageData.loadData()
manageData.sortData(TravellingPlane(sort))
manageData.plotData(name+"_"+sort)

sort = "exact"
manageData.loadData()
manageData.sortData(TravellingPlane(sort))
manageData.plotData(name+"_"+sort)

"""
for name in ["tour_test_1","tour_test_2","matlab_output_10","matlab_output_100","matlab_output_200"]:
	manageData.loadData("matlab/{}.csv".format(name))
	manageData.sortData(TravellingPlane("greedy"))
	manageData.plotData(name)
"""