import shared

from manageData import ManageData
from travellingPlane import TravellingPlane

manageData = ManageData()
numberPoints = [6,10,20,100,200,1000]

#manageData.updateData(numberPoints)
for n in numberPoints:
	print(n)

	name = "test_"+str(n)

	sort = "progressive"
	manageData.loadData(n)
	manageData.sortData(TravellingPlane(sort))
	manageData.plotData(name+"_"+sort)

	sort = "greedy"
	manageData.loadData(n)
	manageData.sortData(TravellingPlane(sort))
	manageData.plotData(name+"_"+sort)

	if (n<=10):
		sort = "exact"
		manageData.loadData(n)
		manageData.sortData(TravellingPlane(sort))
		manageData.plotData(name+"_"+sort)

"""
for name in ["tour_test_1","tour_test_2","matlab_output_10","matlab_output_100","matlab_output_200"]:
	manageData.loadData("matlab/{}.csv".format(name))
	manageData.sortData(TravellingPlane("greedy"))
	manageData.plotData(name)
"""